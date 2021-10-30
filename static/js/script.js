window.onload = function(){
    


    const flag_id_duplicado = document.getElementById("id_duplicado_db");
    
    const txt_id = document.getElementById("input_id");
    const txt_name = document.getElementById("input_name");
    const txt_owner = document.getElementById("input_owner");
    const txt_price = document.getElementById("input_price");

    const btn_create = document.getElementById("create");
    const btn_read = document.getElementById("read");
    const btn_update = document.getElementById("update");
    const btn_delete = document.getElementById("delete");

    console.log(btn_create)
    console.log(btn_read)
    console.log(btn_update)
    console.log(btn_delete)

    btn_create.addEventListener("click", function()
    {
        if (txt_id.value == ""){
            alert("O ID não pode ser Nulo")
            event.preventDefault();
        }
    });

    btn_create.addEventListener("click", function()
    {
        if (txt_name.value == "" ){
            alert("O Nome do Produto não pode ser Nulo")
            event.preventDefault();
        }
    });

    btn_create.addEventListener("click", function()
    {
        if (txt_price.value == "" || parseFloat(txt_price.value).replace(",", ".") < 0.01){
            alert("O Valor não deve ser inferior à R$ 0,01")
            event.preventDefault();
        }
    });

}