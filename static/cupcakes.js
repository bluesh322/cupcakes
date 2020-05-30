const BASE_URL = "http://localhost:5000/api"

/* Given data about a cupcake, generate HTML */

function generateCupcakeHTML(cupcake) {
    return `
    <div data-cupcake-id="${cupcake.id}">
        <li>
            ${cupcake.flavor} | ${cupcake.size} | ${cupcake.rating}
            <button class="delete-button btn btn-secondary">
            X
            </button>
        </li>
        <img class="Cupcake-img"
            src="${cupcake.image}"
            alt="(no image provided)">
    </div>
    `;
}

/** Put initial cupcakes on page */

async function showInitCupcakes() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);
    for (let cupcakeData of response.data.cupcakes) {
        let newCupcake = $(generateCupcakeHTML(cupcakeData));
        $('#cupcakes-list').append(newCupcake);
    }
}

/* Handle form for adding new cupcakes */

$("#new-cupcake-form").on("submit", async function (evt) {
    evt.preventDefault();

    let flavor = $("#flavor").val();
    console.log(flavor + "l1");
    let rating = $("#rating").val();
    let size = $("#size").val();
    let image = $("#image").val();

    const newCupcakeRes = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });
    
    
    let newCupcake = $(generateCupcakeHTML(newCupcakeRes.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
});

/* delete cupcake */

$("#cupcakes-list").on("click", ".delete-button", async function (evt) {
    evt.preventDefault();

    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");
    console.log(cupcakeId);

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();

});

$(showInitCupcakes);