from handlers.start import router as start_router
from handlers.navigation import router as navigation_router
from handlers.main_handlers import router as main_handlers_router
from handlers.tariffs import router as tariffs_router
from handlers.referral import router as referral_router
from handlers.account import router as account_router
from handlers.admin_handlers import router as admin_router
from handlers.join import router as join_router

__all__ = [
    'start_router',
    'navigation_router',
    'main_handlers_router',
    'tariffs_router',
    'referral_router',
    'account_router',
    'admin_router',
    'join_router',
]
