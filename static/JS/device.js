function filterDevices() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("form1");
    filter = input.value.toUpperCase();
    table = document.querySelector(".w3-table-all");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0]; // Assuming deviceID is in the first column

      if (td) {
        txtValue = td.textContent || td.innerText;

        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }

