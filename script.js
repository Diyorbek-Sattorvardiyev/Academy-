document.getElementById("registerForm").addEventListener("submit", function(event) {
    event.preventDefault();

    // Formadan ma'lumotlarni olish
    let formData = new FormData(this);
    let data = new URLSearchParams();

    // Ma'lumotlarni URLSearchParams ga o'zgartirish
    formData.forEach((value, key) => {
        data.append(key, value);
    });

    // Ma'lumotlarni Flask serveriga yuborish
    fetch('/register', {
        method: 'POST',
        body: data
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("message").textContent = data.message;  // Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tganini ko'rsatish
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
