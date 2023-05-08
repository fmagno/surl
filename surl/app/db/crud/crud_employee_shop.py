from app.db.crud.crud_base import CRUDBase
from app.schemas.employee_shop import (
    EmployeeShopLinkDb,
    EmployeeShopLinkDbCreate,
    EmployeeShopLinkDbUpdate,
)


class CRUDEmployeeShop(
    CRUDBase[EmployeeShopLinkDb, EmployeeShopLinkDbCreate, EmployeeShopLinkDbUpdate]
):
    ...


crud_employee_shop = CRUDEmployeeShop(EmployeeShopLinkDb)
