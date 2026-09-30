const display = document.getElementById("display");
const buttons = document.querySelectorAll(".dialer button");

buttons.forEach(button => {
    button.addEventListener("click", () => {

        if (button.id === "delete") {
            display.value = display.value.slice(0, -1);

        } else if (button.id === "enter") {
            console.log("Entered:", display.value);

        } else {
            display.value += button.value;
        }

    });
});