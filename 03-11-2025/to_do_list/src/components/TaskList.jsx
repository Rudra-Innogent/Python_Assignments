import React, { useState } from "react";

function TaskList({ tasks, deleteTask, updateTask }) {
  const [editId, setEditId] = useState(null);
  const [newText, setNewText] = useState("");

  const handleEdit = (id, currentText) => {
    setEditId(id);
    setNewText(currentText);
  };

  const handleUpdate = (id) => {
    updateTask(id, newText);
    setEditId(null);
    setNewText("");
  };

  if (tasks.length === 0)
    return <p className="no-task">No tasks yet. Add one!</p>;

  return (
    <ul className="task-list">
      {tasks.map((task) => (
        <li key={task.id} className="task-item">
          <div>
           
            <p><strong>Date:</strong> {task.date}</p>

            {editId === task.id ? (
              <input
                value={newText}
                onChange={(e) => setNewText(e.target.value)}
              />
            ) : (
              <p><strong>Task:</strong> {task.description}</p>
            )}
          </div>

          <div className="task-buttons">
            {editId === task.id ? (
              <button onClick={() => handleUpdate(task.id)}>Save</button>
            ) : (
              <button onClick={() => handleEdit(task.id, task.description)}>
                Edit
              </button>
            )}
            <button onClick={() => deleteTask(task.id)}>Delete</button>
          </div>
        </li>
      ))}
    </ul>
  );
}

export default TaskList;
