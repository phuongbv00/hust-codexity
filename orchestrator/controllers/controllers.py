from fastapi import APIRouter, HTTPException
from models.itelrationRepair import ItelrationRepairInput
from models.preshotRepair import PreshotRepairInput
from service.itelrationRepairService import ItelrationRepairService
from service.commonService import CommonService

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/iteration-repair")
async def iteration_repair(request: ItelrationRepairInput):
    common_service = CommonService()
    itelrationRepairService = ItelrationRepairService(common_service)
    return itelrationRepairService.itelrationRepair(request)

@router.get("/preshot-repair")
async def preshot_repair(request: PreshotRepairInput):
    return "anhvu"