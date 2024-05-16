function eliminarPelicula(id){
    Swal.fire({
        title:"Seguro de eliminar",
        showDenyButton:true,
        confirmButtonText :"SI",
        denyButtonText : "NO",
    }).then((result)=>{
        if (result.isConfirmed){
            location.href ="/eliminarPelicula/"+id
        }
    })
}

