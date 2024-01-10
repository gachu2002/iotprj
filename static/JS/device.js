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

  function populateDeviceTable(apikey) {
    var tableBody = document.getElementById("deviceTableBody");

    // Use Fetch API to make a GET request to your API endpoint
    fetch("/api/" + apikey + "/listdevices")
      .then(response => response.json())
      .then(data => {
        // Clear the existing table rows
        tableBody.innerHTML = "";

        // Iterate through the data and create table rows
        data.forEach(device => {
          var row = tableBody.insertRow();
          row.insertCell(0).textContent = device.deviceID;
          row.insertCell(1).textContent = device.name;
          row.insertCell(2).textContent = device.type;
          row.insertCell(3).textContent = device.description;
          // You can add actions or links in the last cell if needed
          row.insertCell(4).innerHTML = '<a href="#" class="view" title="View" data-toggle="tooltip"><i class="fa fa-eye w3-blue">&#xE417;</i></a>' +
            '<a href="#" class="edit" title="Edit" data-toggle="tooltip"><i class="fa fa-pencil-square w3-yellow">&#xE254;</i></a>' +
            '<a href="#" class="delete" title="Delete" data-toggle="tooltip"><i class="fa fa-trash w3-red">&#xE872;</i></a>';
        });
      })
      .catch(error => console.error("Error fetching data:", error));
  }

  // Call the function with the appropriate API key
  populateDeviceTable("your_api_key");