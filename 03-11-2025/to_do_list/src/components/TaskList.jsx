import React, { useState } from "react";

function TaskList({ tasks, updateTask, deleteTask }) {  // receiving props from ToDoList.jsx named as tasks, updateTask and deleteTask
  const [editId, setEditId] = useState(null);         // state to track which task is being edited and its initial value is null
  const [newDesc, setNewDesc] = useState("");       // state to track new description of the task being edited and its initial value is empty string

  const handleEdit = (id, desc) => { // When Edit button is clicked
    setEditId(id);
    setNewDesc(desc);
  };

  const handleSave = (id) => {    // When Save button is clicked
    updateTask(id, newDesc);    // calling parent function via props defined in ToDoList.jsx named as updateTask and passing id as state and newDesc as updated description
    setEditId(null);        // exit edit mode after saving
  };

  return (
    <ul className="task-list">
      {tasks.map((task) => (
        <li key={task.id} className="task-item">
          {editId === task.id ? (  // If in edit mode, show input field, turnary operator
            <input
              type="text"
              value={newDesc}
              onChange={(e) => setNewDesc(e.target.value)}
              className="edit-input"
            />
          ) :                   //else show task description
          (
            <span className="task-desc">{task.description}</span>
          )}        {/* turnary operator ends */}

          <div className="task-footer">
            <span className="task-date">{task.date}</span>

            <div className="task-actions">
              {editId === task.id ? (   // If in edit mode, show Save button
                <button className="save-btn" onClick={() => handleSave(task.id)}> { /* Save button fetches handleSave function defined above */}
                  Save
                </button>
              ) : (  //else show Edit button
                <button
                  className="edit-btn"
                  onClick={() => handleEdit(task.id, task.description)}
                >
                  Edit
                </button>
              )}        {/* turnary operator ends */}
              <button
                className="delete-btn"
                onClick={() => deleteTask(task.id)} // Delete button fetches deleteTask function from props defined in ToDoList.jsx named as deleteTask
              >
                Delete
              </button>
            </div>
          </div>
        </li>
      ))}
    </ul>
  );
}

export default TaskList;
