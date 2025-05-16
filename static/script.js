document.getElementById("get-task-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const id = document.getElementById("task-id").value;
    if (id) {
        window.location.href = `/tasks/${id}`;
    }
});

document.getElementById('patch-task-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const taskId = document.getElementById('patch-task-id').value.trim();
    const title = document.getElementById('patch-title').value.trim();
    const description = document.getElementById('patch-description').value.trim();

    if (!taskId || isNaN(taskId)) {
        alert("Пожалуйста, введите корректный ID задачи");
        return;
    }

    const body = {};
    if (title) body.title = title;
    if (description) body.description = description;

    try {
        const response = await fetch(`/tasks/${taskId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (response.ok) {
            const updatedTask = await response.json();
            alert(
                `Задача обновлена:\n` +
                `ID: ${updatedTask.id}\n` +
                `Title: ${updatedTask.title}\n` +
                `Description: ${updatedTask.description}\n` +
                `Created at: ${updatedTask.created_at}\n` +
                `Updated at: ${updatedTask.updated_at}`
            );
        } else {
            const errorData = await response.json();
            alert("Ошибка при обновлении задачи: " + (errorData.detail || response.statusText));
        }
    } catch (error) {
        alert("Ошибка сети или сервера: " + error.message);
    }
});

document.getElementById('delete-task-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const taskId = document.getElementById('delete-task-id').value;
    try{
        const response = await fetch(`/tasks/${taskId}`, {
            method: 'DELETE',
        });

        if (response.ok){
            const deleteTask = await response.json();
                if (deleteTask.result){
                    alert("Задача успешно удалилась")
                } else {
                    alert("Задача не удалена")
                }
        } else {
            alert("Задача не удалена")
        }
    } catch (error) {
        alert("Ошибка сети или сервера: " + error.message);
    }
});