from .models import User, Task
from .database import async_session
from sqlalchemy import select, update, delete, and_


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper


# Создание юзера
@connection
async def setUser(session, name: str, surname: str) -> None:
    try:
        user = User(name=name, 
                    surname=surname
                    )
        
        session.add(user)
        await session.commit()

    except Exception as e:
        print(f"Error set User - {e}")


# Создание задачи
@connection
async def setTask(session, title: str, user_name: str, user_surname: str, description: str = None) -> list:
    try:
        task = Task(
                    title=title, 
                    description=description,  
                    user_name=user_name, 
                    user_surname=user_surname
                )
        
        session.add(task)
        await session.flush()
        await session.commit()

        return [{
            "id": task.id, 
            "title": title,
            "description": description, 
            "created_at": task.created_at, 
            "updated_at": task.updated_at, 
            "user_name": user_name, 
            "user_surname": user_surname,
        }]
    
    except Exception as e:
        print(f"Error set Task - {e}")
        return []


# Получение всех задач
@connection
async def getTasksAll(session) -> list:
    try:
        tasks = await session.scalars(select(Task))
        if tasks:
            result = []
            for task in tasks:
                result.append({
                            "id": task.id, 
                            "title": task.title, 
                            "description": task.description, 
                            "created_at": task.created_at, 
                            "updated_at": task.updated_at,
                            "user_name": task.user_name, 
                            "user_surname": task.user_surname,
                        })
                
            return result
        
        return []
    except Exception as e:
        print(f"Error get tasks - {e}")
        return []
    

# Получение задач юзера
@connection
async def getTasksUser(session, user_name: str, user_surname: str) -> list:
    try:
        tasks = await session.scalars(select(Task).where(and_(Task.user_name == user_name, Task.user_surname == user_surname)))
        if tasks:
            result = []
            for task in tasks:
                result.append({
                            "id": task.id, 
                            "title": task.title, 
                            "description": task.description, 
                            "created_at": task.created_at, 
                            "updated_at": task.updated_at,
                            "user_name": task.user_name, 
                            "user_surname": task.user_surname,
                        })
                
            return result
        
        return []
    except Exception as e:
        print(f"Error get user tasks - {e}")
        return []
    
# Получение задачи по id
@connection
async def getTask(session, idTask: int) -> dict:
    print(idTask)
    try:
        task = await session.scalar(select(Task).where(Task.id == idTask))
        if task:
            return {
                "id": task.id, 
                "title": task.title, 
                "description": task.description, 
                "created_at": task.created_at, 
                "updated_at": task.updated_at,  
            }
        
        return {}
    except Exception as e:
        print(f"Error get task - {e}")
        return {}
    
    
# Обновление задачи
@connection
async def updateTask(session, idTask: int, title: str = None, description: str = None) -> dict:
    try:
        if title and description:
            task = update(Task).where(Task.id == idTask).values(title=title, description=description)
        elif title:
            task = update(Task).where(Task.id == idTask).values(title=title)
        elif description:
            task = update(Task).where(Task.id == idTask).values(description=description)
        else:
            return {}

        result = await session.execute(task)

        if result.rowcount > 0:
                task = await session.scalar(select(Task).where(Task.id == idTask))
                await session.commit()
        else:
            await session.rollback()


        return {
            "id": task.id, 
            "title": task.title, 
            "description": task.description, 
            "created_at": task.created_at, 
            "updated_at": task.updated_at,  
        }
    except Exception as e:
        await session.rollback()
        print(f"Error update task - {e}")
        return {}
    

 # Удаление задачи   
@connection
async def deleteTask(session, idTask: int) -> bool:
    try:
        task = delete(Task).where(Task.id == idTask)
        result = await session.execute(task)

        if result.rowcount > 0:
            await session.commit()
            return True
        
        await session.rollback()

        return False
    except Exception as e:
        await session.rollback()
        print(f"Error delete task - {e}")
        return False
    

