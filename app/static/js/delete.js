function DeleteConfirm(event) {  
    event.preventDefault(); // Evita que o link seja seguido imediatamente  
    var choice = confirm("Você tem certeza que deseja deletar sua conta?");  
    if (choice) {  
        document.getElementById("DeleteChoice").submit();  
    }  
}