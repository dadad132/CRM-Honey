"""
IT Knowledge Base Seeder

Seeds the database with comprehensive IT troubleshooting articles,
categories, and diagnostic trees if they don't already exist.
Imports data from the kb_data package (12 categories, 190+ articles).
"""
import logging
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import engine
from app.models.support_kb import SupportArticle, SupportCategory
from app.models.knowledge_base import KBDiagnosticTree

logger = logging.getLogger(__name__)


async def seed_knowledge_base(workspace_id: int) -> None:
    """Seed the KB if the tables are empty for this workspace."""
    async with AsyncSession(engine) as session:
        # Check if already seeded
        existing = (await session.execute(
            select(SupportArticle).where(SupportArticle.workspace_id == workspace_id).limit(1)
        )).scalar_one_or_none()
        if existing:
            return  # Already seeded

        # Import data (deferred to avoid circular imports at module level)
        from app.core.kb_data import ALL_ARTICLES, ALL_DIAGNOSTIC_TREES, CATEGORIES

        # ── 1. Seed categories ──────────────────────────────────────
        for cat in CATEGORIES:
            session.add(SupportCategory(
                workspace_id=workspace_id,
                name=cat["name"],
                icon=cat["icon"],
                description=cat.get("description", ""),
                article_count=0,
            ))
        await session.flush()

        # Build a quick name -> id lookup
        rows = (await session.execute(
            select(SupportCategory).where(SupportCategory.workspace_id == workspace_id)
        )).scalars().all()
        cat_map: dict[str, int] = {c.name: c.id for c in rows}

        # ── 2. Seed articles ────────────────────────────────────────
        cat_counts: dict[str, int] = {}
        for art in ALL_ARTICLES:
            session.add(SupportArticle(
                workspace_id=workspace_id,
                category=art["category"],
                problem_title=art["problem_title"],
                problem_description=art["problem_description"],
                problem_keywords=art["problem_keywords"],
                solution_steps=art["solution_steps"],
                solution_source="manual",
                is_verified=True,
                is_active=True,
            ))
            cat_counts[art["category"]] = cat_counts.get(art["category"], 0) + 1

        # Update cached article counts on each category
        for cat_name, count in cat_counts.items():
            if cat_name in cat_map:
                cat_obj = await session.get(SupportCategory, cat_map[cat_name])
                if cat_obj:
                    cat_obj.article_count = count

        # ── 3. Seed diagnostic trees ────────────────────────────────
        for tree_def in ALL_DIAGNOSTIC_TREES:
            await _seed_tree_node(
                session,
                workspace_id,
                tree_def["category"],
                tree_def["root"],
                parent_id=None,
                sort_order=0,
            )

        await session.commit()
        logger.info(
            f"✅ Seeded IT Knowledge Base: {len(ALL_ARTICLES)} articles, "
            f"{len(CATEGORIES)} categories, {len(ALL_DIAGNOSTIC_TREES)} diagnostic trees"
        )


async def _seed_tree_node(
    session: AsyncSession,
    workspace_id: int,
    category: str,
    node: dict,
    parent_id: int | None,
    sort_order: int,
) -> None:
    """Recursively insert a diagnostic-tree node and its children."""
    db_node = KBDiagnosticTree(
        workspace_id=workspace_id,
        parent_id=parent_id,
        title=node["title"],
        node_type=node.get("node_type", "question"),
        question_text=node.get("question_text"),
        solution_text=node.get("solution_text"),
        category=category,
        sort_order=sort_order,
        is_active=True,
    )
    session.add(db_node)
    await session.flush()  # get db_node.id

    for idx, child in enumerate(node.get("children", [])):
        await _seed_tree_node(
            session, workspace_id, category, child,
            parent_id=db_node.id, sort_order=idx,
        )
