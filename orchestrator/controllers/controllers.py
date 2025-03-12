from fastapi import APIRouter, HTTPException
from models.itelrationRepair import ItelrationRepairInput
from models.preshotRepair import PreshotRepairInput
from service.itelrationRepairService import ItelrationRepairService
from service.preshotRepairService import PreshotRepairService
from service.commonService import CommonService

router = APIRouter()
common_service = CommonService()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/iteration-repair")
async def iteration_repair(request: ItelrationRepairInput):
    itelrationRepairService = ItelrationRepairService(common_service)
    return await itelrationRepairService.itelrationRepair(request)

@router.post("/preshot-repair")
async def preshot_repair(request: PreshotRepairInput):
    preshotRepairService = PreshotRepairService(common_service)
    return await preshotRepairService.preshotRepair(request)