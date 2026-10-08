const display = document.getElementById("display");
const buttons = document.querySelectorAll(".buttons button");
const cardNumberInput = document.getElementById("card-number");
const cardNumberDisplay = document.getElementById("card-number-display");
const cardStatus = document.getElementById("card-status");
const cardNumpadButtons = document.querySelectorAll(".card-numpad button");
const maxCardNumberLength = 6;
const bankCard = document.querySelector(".bank-card");
const cardReaderSlot = document.querySelector(".card-reader-slot");
const display1 = document.getElementById("display1");
const hifadhiLogo = document.getElementById("hifadhi-logo");
const atmMenu = document.getElementById("atm-menu");
const atmMenuTitle = document.getElementById("atm-menu-title");
const atmMenuOptions = document.getElementById("atm-menu-options");
const atmMessage = document.getElementById("atm-message");
const ejectCardButton = document.getElementById("eject-card");
let logoRevealTimer;
let atmState = "locked";
let currentCardNumber = null;
let currentPin = null;

function revealHifadhiLogo() {
    display1.classList.add("has-logo");
    hifadhiLogo.hidden = false;
    requestAnimationFrame(() => hifadhiLogo.classList.add("is-visible"));
}

function showMenu(message = "") {
    atmState = "menu";
    display.type = "text";
    display.value = "";
    display.placeholder = "Select 1-4, then press Enter";
    atmMenuTitle.textContent = "Select a transaction";
    atmMenuOptions.hidden = false;
    atmMessage.textContent = message;
}

async function handleEnter() {
    const value = display.value.trim();

    if (atmState === "pin") {
        if (!value) {
            atmMessage.textContent = "Enter your PIN";
            return;
        }

        const response = await fetch("http://127.0.0.1:8000/authenticate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ card_number: currentCardNumber, pin: value })
        });
        const result = await response.json();
        if (!response.ok || !result.authenticated) {
            display.value = "";
            atmMessage.textContent = result.message || "Authentication failed";
            return;
        }

        currentPin = value;
        showMenu(`Welcome, ${result.name}`);
        return;
    }

    if (atmState === "menu") {
        if (value === "1" || value === "2") {
            atmState = value === "1" ? "deposit" : "withdraw";
            display.value = "";
            display.placeholder = "Enter amount, then press Enter";
            atmMenuTitle.textContent = `Enter ${atmState} amount`;
            atmMenuOptions.hidden = true;
            atmMessage.textContent = "";
        } else if (value === "3") {
            ejectCardButton.click();
        } else if (value === "4") {
            const response = await fetch("http://127.0.0.1:8000/balance", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ card_number: currentCardNumber, pin: currentPin })
            });
            const result = await response.json();
            if (!response.ok || !result.success) {
                atmMessage.textContent = result.message || "Could not retrieve balance";
                return;
            }

            showMenu(`Current balance: $${Number(result.balance).toFixed(2)}`);
        } else {
            atmMessage.textContent = "Choose 1, 2, 3, or 4";
        }
        return;
    }

    if (atmState === "deposit" || atmState === "withdraw") {
        const amount = Number(value);
        if (!Number.isFinite(amount) || amount <= 0) {
            atmMessage.textContent = "Enter an amount greater than zero";
            return;
        }

        const response = await fetch(`http://127.0.0.1:8000/transactions/${atmState}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                card_number: currentCardNumber,
                pin: currentPin,
                amount
            })
        });
        const result = await response.json();
        if (!response.ok || !result.success) {
            atmMessage.textContent = result.message || "Transaction failed";
            return;
        }

        showMenu(`${result.message}. Balance: $${Number(result.balance).toFixed(2)}`);
    }
}

buttons.forEach(button => {
    button.addEventListener("click", async () => {
        if (atmState === "locked" || atmState === "inserting") {
            return;
        }

        if (button.id === "delete") {
            display.value = display.value.slice(0, -1);
        } else if (button.id === "enter") {
            try {
                await handleEnter();
            } catch (error) {
                atmMessage.textContent = "Could not complete the request. Check the banking API.";
                console.error("ATM request failed:", error);
            }
        } else if (/^\d+$/.test(button.value) && display.value.length < 10) {
            display.value += button.value;
        }
    });
});

cardNumpadButtons.forEach(button => {
    button.addEventListener("click", () => {
        if (button.dataset.action === "clear") {
            cardNumberInput.value = "";
        } else if (button.dataset.action === "delete") {
            cardNumberInput.value = cardNumberInput.value.slice(0, -1);
        } else if (cardNumberInput.value.length < maxCardNumberLength) {
            cardNumberInput.value += button.dataset.digit;
        }
    });
});

cardNumberInput.addEventListener("input", () => {
    cardNumberInput.value = cardNumberInput.value.replace(/\D/g, "").slice(0, maxCardNumberLength);
});

document.querySelector(".card-form").addEventListener("submit", async event => {
    event.preventDefault();
    if (bankCard.classList.contains("is-inserting") || bankCard.classList.contains("is-ejecting")) {
        return;
    }

    const enteredCardNumber = cardNumberInput.value;
    const submitButton = event.currentTarget.querySelector('button[type="submit"]');
    cardStatus.textContent = "Checking card...";
    cardStatus.dataset.state = "checking";
    submitButton.disabled = true;

    try {
        const response = await fetch("http://127.0.0.1:8000/card-number", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ card_number: enteredCardNumber })
        });
        if (!response.ok) {
            throw new Error(`Card number request failed: ${response.status}`);
        }

        const result = await response.json();
        if (!result.accepted) {
            cardStatus.textContent = result.message || "Card number not recognized";
            cardStatus.dataset.state = "error";
            return;
        }

        cardStatus.textContent = result.message;
        cardStatus.dataset.state = "success";

        currentCardNumber = enteredCardNumber;
        atmState = "inserting";
        cardNumberDisplay.textContent = enteredCardNumber.match(/.{1,4}/g).join("-");
        cardNumberInput.value = "";
        window.clearTimeout(logoRevealTimer);
        hifadhiLogo.hidden = true;
        hifadhiLogo.classList.remove("is-visible");
        display1.classList.remove("has-logo");
        ejectCardButton.hidden = true;

        const cardBounds = bankCard.getBoundingClientRect();
        const slotBounds = cardReaderSlot.getBoundingClientRect();
        const horizontalTravel = slotBounds.left + slotBounds.width / 2 - (cardBounds.left + cardBounds.width / 2);
        const verticalTravel = slotBounds.top + slotBounds.height / 2 - (cardBounds.top + cardBounds.height / 2);

        bankCard.style.setProperty("--insert-x", `${horizontalTravel}px`);
        bankCard.style.setProperty("--insert-y", `${verticalTravel}px`);
        bankCard.addEventListener("animationend", animationEvent => {
            if (animationEvent.animationName !== "card-insertion") {
                return;
            }

            ejectCardButton.hidden = false;
            atmState = "pin";
            display.type = "password";
            display.value = "";
            display.placeholder = "Enter PIN, then press Enter";
            atmMenu.hidden = false;
            atmMenuTitle.textContent = "Enter your PIN";
            atmMenuOptions.hidden = true;
            atmMessage.textContent = "";
            display1.classList.add("has-menu");
        }, { once: true });
        bankCard.classList.add("is-inserting");
    } catch (error) {
        cardStatus.textContent = "Could not verify the card. Check that the banking API is running.";
        cardStatus.dataset.state = "error";
        console.error("Could not verify card with the banking API:", error);
    } finally {
        submitButton.disabled = false;
    }
});

ejectCardButton.addEventListener("click", () => {
    if (!bankCard.classList.contains("is-inserting")) {
        return;
    }

    bankCard.classList.remove("is-inserting");
    bankCard.classList.add("is-ejecting");
    ejectCardButton.disabled = true;
    atmState = "locked";
    currentCardNumber = null;
    currentPin = null;
    window.clearTimeout(logoRevealTimer);
    hifadhiLogo.hidden = true;
    hifadhiLogo.classList.remove("is-visible");
    atmMenu.hidden = true;
    display1.classList.remove("has-menu");
    display1.classList.remove("has-logo");

    bankCard.addEventListener("animationend", animationEvent => {
        if (animationEvent.animationName !== "card-ejection") {
            return;
        }

        bankCard.classList.remove("is-ejecting");
        bankCard.style.removeProperty("--insert-x");
        bankCard.style.removeProperty("--insert-y");
        cardNumberDisplay.textContent = "";
        display.type = "text";
        display.value = "";
        display.placeholder = "HIFADHI";
        atmMenuOptions.hidden = false;
        atmMessage.textContent = "";
        ejectCardButton.disabled = false;
        ejectCardButton.hidden = true;
        logoRevealTimer = window.setTimeout(revealHifadhiLogo, 3000);
    }, { once: true });
});