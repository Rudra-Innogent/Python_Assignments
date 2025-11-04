import React from "react";

function DeleteTask({ id, deleteTask }) { // receiving props from ToDoList.jsx named as id
  return (
    <button
      className="delete-btn"
      onClick={() => deleteTask(id)}
    >
      Delete
    </button>
  );
}
   
export default DeleteTask;
