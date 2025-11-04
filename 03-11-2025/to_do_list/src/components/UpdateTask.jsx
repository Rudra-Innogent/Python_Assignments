import React from "react";

function UpdateTask({ id, newText, handleUpdate }) {
  return (
    <button
      className="save-btn"
      onClick={() => handleUpdate(id, newText)}
    >
      Save
    </button>
  );
}

export default UpdateTask;
