function toggleSidebar(){
    document.getElementById("sidebar").classList.toggle("hide");
}

/* ================= MODAL FIX ================= */

function openModal(id) {

    // 🔥 CLOSE ALL MODALS FIRST
    document.querySelectorAll(".modal").forEach(modal => {
        modal.style.display = "none";
    });

    // OPEN SELECTED MODAL
    document.getElementById(id).style.display = "flex";
}

function closeModal(id) {
    document.getElementById(id).style.display = "none";
}