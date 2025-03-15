from fastapi import APIRouter, HTTPException
from models.itelrationRepair import ItelrationRepairInput
from models.preshotRepair import PreshotRepairInput
from service.itelrationRepairService import ItelrationRepairService
from service.preshotRepairService import PreshotRepairService
from service.commonService import CommonService
from service.dataConstruction import DataConstruction

router = APIRouter()
common_service = CommonService()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/iteration-repair")
def iteration_repair(request: ItelrationRepairInput):
    itelrationRepairService = ItelrationRepairService(common_service)
    return itelrationRepairService.itelrationRepair(request)

@router.post("/preshot-repair")
def preshot_repair(request: PreshotRepairInput):
    preshotRepairService = PreshotRepairService(common_service)
    return preshotRepairService.preshotRepair(request)

@router.post("/data-construction")
def data_construction():
    dataConstruction = DataConstruction(common_service)
    return dataConstruction.createData()

@router.post("/test")
def data_construction():
    itelrationRepairService = ItelrationRepairService(common_service)
    return itelrationRepairService.codexity()
