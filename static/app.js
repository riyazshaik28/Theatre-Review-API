const API_URL = "http://localhost:8000";

const reviewForm = document.getElementById("reviewForm");
const reviewIdField = document.getElementById("reviewId");
const reviewList = document.getElementById("reviewList");
const summaryContainer = document.getElementById("summaryContainer");
const searchInput = document.getElementById("searchInput");
const playFilter = document.getElementById("playFilter");
const sortBy = document.getElementById("sortBy");
const refreshButton = document.getElementById("refreshButton");
const submitButton = document.getElementById("submitReviewButton");
const cancelEditButton = document.getElementById("cancelEditButton");
const formHeading = document.getElementById("formHeading");

let allReviews = [];

function escapeHtml(value = "") {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

async function fetchJson(url, options = {}) {
  const response = await fetch(`${API_URL}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Request failed");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

function resetForm() {
  reviewForm.reset();
  reviewIdField.value = "";
  submitButton.textContent = "Add review";
  formHeading.textContent = "Submit a review";
  cancelEditButton.classList.add("hidden");
}

function populateForm(review) {
  reviewForm.play_name.value = review.play_name;
  reviewForm.reviewer_name.value = review.reviewer_name;
  reviewForm.rating.value = String(review.rating);
  reviewForm.comment.value = review.comment;
  reviewIdField.value = String(review.id);
  submitButton.textContent = "Update review";
  formHeading.textContent = "Edit review";
  cancelEditButton.classList.remove("hidden");
}

function renderReviews(reviews) {
  allReviews = reviews;

  if (!reviews.length) {
    reviewList.innerHTML = '<div class="empty-state">No reviews match the current filters.</div>';
    return;
  }

  reviewList.innerHTML = reviews
    .map(
      (review) => `
        <article class="review-card">
          <div class="review-header">
            <h3>${escapeHtml(review.play_name)}</h3>
            <span class="rating-badge">${review.rating}/5</span>
          </div>
          <div class="meta">By ${escapeHtml(review.reviewer_name)} • ${new Date(review.created_at).toLocaleDateString()}</div>
          <p>${escapeHtml(review.comment)}</p>
          <div class="review-actions">
            <button class="secondary-btn edit-btn" data-id="${review.id}" type="button">Edit</button>
            <button class="danger-btn delete-btn" data-id="${review.id}" type="button">Delete</button>
          </div>
        </article>
      `
    )
    .join("");
}

function renderSummary(summary) {
  if (!summary.length) {
    summaryContainer.innerHTML = '<div class="empty-state">No play summaries yet.</div>';
    return;
  }

  summaryContainer.innerHTML = summary
    .map(
      (entry) => `
        <div class="summary-card">
          <strong>${escapeHtml(entry.play_name)}</strong>
          <div>Average: ${entry.average_rating}/5</div>
          <div>Total reviews: ${entry.total_reviews}</div>
        </div>
      `
    )
    .join("");
}

async function loadPlayNames() {
  try {
    const data = await fetchJson("/review/plays");
    const options = ['<option value="">All plays</option>'];
    data.play_names.forEach((name) => {
      options.push(`<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`);
    });
    playFilter.innerHTML = options.join("");
  } catch (error) {
    console.error(error);
  }
}

async function loadReviews() {
  const playName = playFilter.value;
  const search = searchInput.value.trim();
  const query = new URLSearchParams({
    sort_by: sortBy.value,
    limit: 20,
  });

  if (playName) query.set("play_name", playName);
  if (search) query.set("search", search);

  const reviews = await fetchJson(`/review/get?${query.toString()}`);
  renderReviews(reviews);
}

async function loadSummary() {
  const summary = await fetchJson("/review/summary");
  renderSummary(summary);
}

reviewForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = Object.fromEntries(new FormData(reviewForm));
  const payload = {
    ...formData,
    rating: Number(formData.rating),
  };

  try {
    const reviewId = reviewIdField.value;
    if (reviewId) {
      await fetchJson(`/review/getbyid/${reviewId}`, {
        method: "PATCH",
        body: JSON.stringify(payload),
      });
    } else {
      await fetchJson("/review/", {
        method: "POST",
        body: JSON.stringify(payload),
      });
    }

    resetForm();
    await loadReviews();
    await loadSummary();
    await loadPlayNames();
  } catch (error) {
    alert(error.message);
  }
});

reviewList.addEventListener("click", async (event) => {
  const editButton = event.target.closest(".edit-btn");
  if (editButton) {
    const review = allReviews.find((item) => String(item.id) === editButton.dataset.id);
    if (review) {
      populateForm(review);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
    return;
  }

  const deleteButton = event.target.closest(".delete-btn");
  if (deleteButton) {
    const reviewId = deleteButton.dataset.id;
    const confirmed = window.confirm("Delete this review?");
    if (!confirmed) return;

    try {
      await fetchJson(`/review/deletebyid/${reviewId}`, { method: "DELETE" });
      await loadReviews();
      await loadSummary();
      await loadPlayNames();
      if (reviewIdField.value === reviewId) resetForm();
    } catch (error) {
      alert(error.message);
    }
  }
});

cancelEditButton.addEventListener("click", resetForm);
searchInput.addEventListener("input", loadReviews);
playFilter.addEventListener("change", loadReviews);
sortBy.addEventListener("change", loadReviews);
refreshButton.addEventListener("click", async () => {
  await loadSummary();
  await loadPlayNames();
  await loadReviews();
});

resetForm();
loadSummary();
loadPlayNames();
loadReviews();
