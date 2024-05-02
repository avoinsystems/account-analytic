import logging

from odoo.tools import SQL, table_exists

_logger = logging.getLogger(__name__)

def migrate(cr, installed_version):
    _logger.info("Migrating stock analytic data...")
    need_tag_migration = (
        table_exists(cr, "account_analytic_tag_stock_move_rel")
        and cr.execute(
            SQL(
                """
                SELECT COUNT(*)
                FROM account_analytic_tag_stock_move_rel
                """,
            ),
        )
        and cr.fetchall()[0][0] == 0
    )
    assert not need_tag_migration, "analytic tag migration not implemented"
    cr.execute("""
        UPDATE stock_move
        SET analytic_distribution = ('{"' || analytic_account_id || '": 100' || '}')::jsonb
    """)
    cr.execute("""
        UPDATE stock_move_line
        SET analytic_distribution = ('{"' || analytic_account_id || '": 100' || '}')::jsonb
    """)
