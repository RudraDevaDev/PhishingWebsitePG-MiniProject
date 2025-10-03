function sendFeedback(id, status) {
  fetch(`/feedback/${id}/${status}`, { method: "POST" })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        location.reload(); // refresh table after update
      }
    })
    .catch(err => console.error(err));
}