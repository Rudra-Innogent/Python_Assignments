import React from "react";

function UpdateTask({ id, newText, handleUpdate }) { // receiving props from ToDoList.jsx named as id, newText and handleUpdate
  return (
    <button
      className="save-btn"
      onClick={() => handleUpdate(id, newText)} // calling parent function via props defined in ToDoList.jsx
    >
      
    </button>
  );
}

export default UpdateTask;
