const { createApp, ref } = Vue;

createApp({
  setup() {
    const message = ref("Hello Vue!");
    const test = ref("test");
    const email = ref("");
    const password = ref("");
    const confirm_password = ref("");
    const nomatch = ref(false);
    const mode = ref("signup");
    const showError = ref(false);
    function checkEmail() {
      showError.value = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value);
    }
    async function signup() {
      if (password.value !== confirm_password.value) {
        console.error("Passwords do not match");
        nomatch.value = true;
        password.value = "";
        confirm_password.value = "";
        return;
      } else {
        try {
          const response = await fetch("/signup", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: email.value,
              password: password.value,
            }),
          });
          const data = await response.json();
          console.log(data);
          nomatch.value = false;
          email.value = "";
          password.value = "";
          confirm_password.value = "";
          return data;
        } catch (error) {
          console.error("Error signing up:", error);
        }
      }
    }

    async function login() {
      try {
        const response = await fetch("/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email.value,
            password: password.value,
          }),
        });
        const data = await response.json();
        if (!response.ok) {
          console.error("Login failed:", data.error);
          return;
        }
        email.value = "";
        password.value = "";
        window.location.href = "/logintest";
      } catch (error) {
        console.error("Error signing in:", error);
      }
    }

    async function signout() {
      try {
        const response = await fetch("/signout", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });

        const data = await response.json();

        if (!response.ok) {
          console.error("Logout failed:", data.error);
          return;
        }
        window.location.href = "/";
      } catch (error) {
        console.error("Error logging out:", error);
      }
    }

    async function fetchHealth() {
      try {
        const response = await fetch("/health");
        const data = await response.json();
        return data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }
    return {
      message,
      test,
      email,
      password,
      confirm_password,
      signup,
      login,
      nomatch,
      mode,
      checkEmail,
      showError,
      signout,
    };
  },
}).mount("#app");
