document.addEventListener("DOMContentLoaded", function () {
  const deleteButtons = document.querySelectorAll(
    '[data-modal-toggle="delete-student"]'
  );
  const deleteModal = document.getElementById("delete-student");
  const deleteForm = deleteModal.querySelector("form");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const userId = this.getAttribute("data-user-id");
      deleteForm.setAttribute("action", `/student/delete/${userId}`);
    });
  });

  const editButtons = document.querySelectorAll(
    '[data-modal-target="edit-student"]'
  );
  const editModal = document.getElementById("edit-student");
  const editForm = editModal.querySelector("form");
  const studentNameInput = document.getElementById("student_name");
  const studentIdInput = document.getElementById("student_id");

  editButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const studentId = this.getAttribute("data-student-id");
      const studentName = this.getAttribute("data-student-name");

      studentNameInput.value = studentName;
      studentIdInput.value = studentId;

      editForm.setAttribute("action", `/student/edit/${studentId}`)
    });
  });
});
