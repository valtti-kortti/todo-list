from fastapi import APIRouter, HTTPException, Form, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from .schemas import UpdateTaskSchema
from database.crud import (setTask, getTasksUser, getTasksAll,
                            getTask, updateTask, deleteTask)



router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Главная страница
@router.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Создания задачи
@router.post("/tasks", response_class=HTMLResponse)
async def create_tasks(
    request: Request,
    title: str = Form(...),
    user_name: str = Form(...),
    user_surname: str = Form(...),
    description: str = Form(None)):

    try:
        result = await setTask(
                    title = title, 
                    user_name = user_name, 
                    user_surname = user_surname, 
                    description = description,

                )
        
        if result:
            return templates.TemplateResponse("tasks.html", {"request": request, "tasks": result})
        
        raise HTTPException(status_code=500, detail=f"Failed to create task")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task - {e}")
    

# Получение задачи юзера с помощью запроса
@router.get("/tasks", response_class=HTMLResponse)
async def get_tasks_user(
    request: Request,
    name: str = Query(...), 
    surname: str = Query(...)):

    try:
        result = await getTasksUser(user_name=name, user_surname=surname)

        if not result:
            raise HTTPException(status_code=404, detail=f"Tasks not found")
        
        return templates.TemplateResponse("tasks.html", {"request": request, "tasks": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tasks  - {e}")
    

# Получение всех задач
@router.get("/tasks/all")
async def get_all_tasks(request: Request):
    try:
        result = await getTasksAll()

        return templates.TemplateResponse("tasks.html", {"request": request, "tasks": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tasks - {e}")
    

# Получение задачи по ее айди
@router.get("/tasks/{id_task}", response_class=HTMLResponse)
async def get_task_by_id(request: Request, id_task: int):
    try:
        result = await getTask(idTask=id_task)

        if not result:
            raise HTTPException(status_code=404, detail=f"Tasks not found")
        
        return templates.TemplateResponse("task.html", {"request": request, "task": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get task - {e}")
    

# Обновление задачи по айди
@router.patch("/tasks/{id_task}")
async def update_task_by_id(id_task: int, task: UpdateTaskSchema):
    try:
        result = await updateTask(idTask=id_task, title=task.title, description=task.description)

        if not result:
            raise HTTPException(status_code=404, detail=f"Tasks not found")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update task - {e}")
    

# Удаление задачи по айди
@router.delete("/tasks/{id_task}")
async def delete_task_by_id(id_task: int):
    try:
        result = await deleteTask(idTask=id_task)
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Tasks not found")
        
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete task - {e}")

