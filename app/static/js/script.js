document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.getElementById("hamburger");
  const sidebar = document.getElementById("sidebar");

  if (hamburger && sidebar) {
    hamburger.addEventListener("click", () => {
      sidebar.classList.toggle("open");
    });
  }

  // Profile dropdown toggle
  const profileBtn = document.getElementById("profileBtn");
  const dropdownMenu = document.querySelector(".dropdown-menu");

  if (profileBtn && dropdownMenu) {
    profileBtn.addEventListener("click", () => {
      const isExpanded = profileBtn.getAttribute("aria-expanded") === "true";
      profileBtn.setAttribute("aria-expanded", !isExpanded);
      dropdownMenu.hidden = !dropdownMenu.hidden;
    });

    // Close dropdown on outside click
    document.addEventListener("click", (e) => {
      if (!profileBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
        profileBtn.setAttribute("aria-expanded", false);
        dropdownMenu.hidden = true;
      }
    });
  }

  // Notification button - placeholder
  const notifBtn = document.getElementById("notifBtn");
  if (notifBtn) {
    notifBtn.addEventListener("click", () => {
      alert("No new notifications.");
    });
  }

  // Search button functionality
  const searchBtn = document.querySelector(".search-container button");
  const searchInput = document.getElementById("searchInput");
  if (searchBtn && searchInput) {
    searchBtn.addEventListener("click", () => {
      alert(`Searching for "${searchInput.value}"...`);
    });
  }

  // Dark Mode Toggle
  const darkToggle = document.getElementById("darkModeToggle");
  if (darkToggle) {
    // Load saved preference
    const isDark = localStorage.getItem("dark-mode") === "true";
    if (isDark) {
      document.body.classList.add("dark-mode");
      darkToggle.checked = true;
    }

    darkToggle.addEventListener("change", () => {
      document.body.classList.toggle("dark-mode");
      localStorage.setItem("dark-mode", document.body.classList.contains("dark-mode"));
    });
  }
});
