document.addEventListener("DOMContentLoaded", function () {
    // Add Product button event listener
    document.getElementById("new-product-form").addEventListener("submit", function (e) {
      e.preventDefault();
      // Collect new product data from form
      var name = document.getElementById("newProductName").value;
      var price = document.getElementById("newProductPrice").value;
      var available = document.getElementById("newProductAvailable").value;
      var shortDescription = document.getElementById("newProductShortDesc").value;
      var longDescription = document.getElementById("newProductLongDesc").value;
      var categoryId = document.getElementById("newProductCategory").value;

      // Fetch call to add new product
      fetch('/seller/inventory/add_new_product', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          'name': name,
          'price': price,
          'available': available,
          'short_description': shortDescription,
          'long_description': longDescription,
          'category_id': categoryId
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            alert("New product added successfully");
            location.reload(); // Reload the page to update the inventory list
          } else {
            alert("Error adding product: this product already exists.");
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert("Failed to add the product.");
        });

      // Close the modal
      $('#newProductModal').modal('hide');
    });

    document.getElementById("add-inventory-btn").addEventListener("click", function () {
      var productId = document.getElementById("product-id").value;
      var quantity = document.getElementById("quantity").value;

      fetch('/seller/inventory/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          'product_id': productId,
          'quantity': quantity
        })
      })
        .then(function (response) {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Server responded with status: ' + response.status);
          }
        })
        .then(function (data) {
          alert(data.message);
          window.location.reload();
        })
        .catch(function (error) {
          console.error('Error adding inventory item:', error);
        });
    });


    function updateInventoryUI(action, productId, newQuantity) {
      if (action === 'delete') {
        // Remove the row for the deleted item
        var row = document.getElementById('inventory-item-' + productId);
        row.parentNode.removeChild(row);
      } else if (action === 'update') {
        // Update the quantity shown in the UI
        var quantityInput = document.getElementById('quantity-' + productId);
        quantityInput.value = newQuantity;
      }
    }

    //Add BRAND NEW PRODUCT
    // Event listener for adding a new product
    document.getElementById("new-product-form").addEventListener("submit", function (e) {
      e.preventDefault();
      // Collect new product data from form
      var name = document.getElementById("newProductName").value;
      var price = document.getElementById("newProductPrice").value;
      var available = document.getElementById("newProductAvailable").value === "true"; // Make sure to match boolean value
      var shortDescription = document.getElementById("newProductShortDesc").value;
      var longDescription = document.getElementById("newProductLongDesc").value;
      var categoryId = document.getElementById("newProductCategory").value;

      // Fetch call to add new product
      fetch('/seller/inventory/add_new_product', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          'name': name,
          'price': price,
          'available': available,
          'short_description': shortDescription,
          'long_description': longDescription,
          'category_id': categoryId
        })
      })
        .then(response => response.json()) // Parse JSON response
        .then(data => {
          //alert(data.message); // Display message from the server
          if (data.status === 'success') {
            location.reload(); // Reload the page to show new product
          }
        })
        .catch(error => {
          console.error('Error adding product:', error);
          alert("Failed to add the product: " + error);
        });
    });
    // Update button event listeners
    document.querySelectorAll('.update-btn').forEach(function (button) {
      button.addEventListener('click', function () {
        var productId = this.getAttribute('data-product-id');
        var quantityInput = document.getElementById('quantity-' + productId);
        var newQuantity = quantityInput.value;

        fetch('/seller/inventory/update', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            'product_id': productId,
            'quantity': newQuantity
          })
        })
          .then(function (response) {
            if (response.ok) {
              return response.json();
            } else {
              throw new Error('Server responded with status: ' + response.status);
            }
          })
          .then(function (result) {
            alert(result.message);
            updateInventoryUI('update', productId, newQuantity);
          })
          .catch(function (error) {
            console.error('Error updating inventory quantity:', error);
            alert('Error updating inventory quantity: ' + error.message);
          });
      });
    });

    // Delete button event listeners
    document.querySelectorAll('.delete-btn').forEach(function (button) {
      button.addEventListener('click', function () {
        var productId = this.getAttribute('data-product-id');
        if (!confirm('Are you sure you want to delete this item?')) {
          return; // Exit if the user does not confirm
        }

        fetch('/seller/inventory/delete', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            'product_id': productId
          })
        })
          .then(response => response.json())
          .then(result => {
            alert(result.message);
            // Call the function to update the UI after deleting an item
            updateInventoryUI('delete', productId);
          })
          .catch(function (error) {
            console.error('Error deleting inventory item:', error);
            alert('Error deleting inventory item: ' + error.message);
          });
      });
    });

    // Update Quantity button event listeners
    var updateButtons = document.querySelectorAll('.update-btn');
    updateButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        var productId = this.getAttribute('data-product-id');
        var quantityInput = document.getElementById('quantity-' + productId);
        var newQuantity = quantityInput.value;

        fetch('/seller/inventory/update', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            'product_id': productId,
            'quantity': newQuantity
          })
        })
          .then(response => response.json())
          .then(result => {
            alert(result.message);
            // Call the function to update the UI after updating an item's quantity
            updateInventoryUI('update', productId, newQuantity);
          })
          .catch(function (error) {
            console.error('Error updating inventory quantity:', error);
            alert('Error updating inventory quantity: ' + error.message);
          });
      });
    });
  });


  // Fetch product sales data and render chart
  fetch('/seller/inventory/product-sales-data')
  .then(response => response.json())
  .then(data => {
      // Render chart using data
  });

   