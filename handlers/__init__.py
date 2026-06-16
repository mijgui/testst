from handlers.start import router as start_router
from handlers.navigation import router as navigation_router
from handlers.tariffs import router as tariffs_router
from handlers.referral import router as referral_router
from handlers.join import router as join_router
from handlers.account import router as account_router
from .start import router as start_router
from .navigation import router as navigation_router
from .tariffs import router as tariffs_router
from .referral import router as referral_router
from .join import router as join_router
from .admin_handlers import router as admin_router   # ← добавить
from .account import router as account_router