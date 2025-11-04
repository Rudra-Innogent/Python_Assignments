import React from "react";

function DeleteTask({ id, deleteTask }) {
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
