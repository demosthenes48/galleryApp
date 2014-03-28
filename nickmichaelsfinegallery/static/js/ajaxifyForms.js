    //generate create, edit, and delete ajax forms

        //art forms

        $('#uploadArtForm').ajaxForm({
            target: '#uploadArtFormMessage',
            success: showResponse
        });

        $('#editArtForm').ajaxForm({
            target: '#editArtFormMessage',
            success: showResponse
        });

        $('#deleteArtForm').ajaxForm({
            target: '#deleteArtFormMessage',
            success: showResponse
        });


        //artist forms

        $('#createArtistForm').ajaxForm({
            target: '#createFormMessage',
            success: showResponse
        });

        $('#editArtistForm').ajaxForm({
            target: '#editFormMessage',
            success: showResponse
        });

        $('#deleteArtistForm').ajaxForm({
            target: '#deleteFormMessage',
            success: showResponse
        });


        //category forms

        $('#createCategoryForm').ajaxForm({
            target: '#createCategoryFormMessage',
            success: showResponse
        });

        $('#editCategoryForm').ajaxForm({
            target: '#editCategoryFormMessage',
            success: showResponse
        });

        $('#deleteCategoryForm').ajaxForm({
            target: '#deleteCategoryFormMessage',
            success: showResponse
        });


        // photo forms

        $('#editPhotoForm').ajaxForm({
            target: '#editPhotoFormMessage',
            success: showResponse
        });

        $('#deletePhotoForm').ajaxForm({
            target: '#deletePhotoFormMessage',
            success: showResponse
        });


    //manage button clicks for modals

        //Art button clicks

        function uploadArtUploadClicked () {
			$('#uploadArtForm').submit();
		};

        function uploadArtCancelClicked () {
			$('#uploadArtModal').modal('hide');
			$('#uploadArtFormMessage').hide();
			clearForm($('#uploadArtForm'));
		};

		function editArtSaveClicked () {
			$('#editArtForm').submit();
		};

		function editArtCancelClicked () {
			$('#editArtModal').modal('hide');
			$('#editArtFormMessage').hide();
			clearForm($('#editArtForm'));
		};

		function deleteArtCancelClicked () {
			$('#deleteArtModal').modal('hide');
			$('#deleteArtFormMessage').hide();
			clearForm($('#deleteArtForm'));
		};

		function deleteArtDeleteClicked () {
			$('#deleteArtForm').submit();
		};


        //Artist button clicks

        function createOKClicked () {
			$('#createArtistForm').submit();
		};

        function createCancelClicked () {
			$('#createArtistModal').modal('hide');
			$('#createFormMessage').hide();
			clearForm($('#createArtistForm'));
		};

		function editSaveClicked () {
			$('#editArtistForm').submit();
		};

		function editCancelClicked () {
			$('#editArtistModal').modal('hide');
			$('#editFormMessage').hide();
			clearForm($('#editArtistForm'));
		};

		function deleteCancelClicked () {
			$('#deleteArtistModal').modal('hide');
			$('#deleteFormMessage').hide();
			clearForm($('#deleteArtistForm'));
		};

		function deleteDeleteClicked () {
			$('#deleteArtistForm').submit();
		};


        //Category button clicks

        function createCategoryOKClicked () {
			$('#createCategoryForm').submit();
		};

        function createCategoryCancelClicked () {
			$('#createCategoryModal').modal('hide');
			$('#createCategoryFormMessage').hide();
			clearForm($('#createCategoryForm'));
		};

		function editCategorySaveClicked () {
			$('#editCategoryForm').submit();
		};

		function editCategoryCancelClicked () {
			$('#editCategoryModal').modal('hide');
			$('#editCategoryFormMessage').hide();
			clearForm($('#editCategoryForm'));
		};

		function deleteCategoryCancelClicked () {
			$('#deleteCategoryModal').modal('hide');
			$('#deleteCategoryFormMessage').hide();
			clearForm($('#deleteCategoryForm'));
		};

		function deleteCategoryDeleteClicked () {
			$('#deleteCategoryForm').submit();
		};


		// Photo button clicks

        function editPhotoSaveClicked () {
			$('#editPhotoForm').submit();
		};

		function editPhotoCancelClicked () {
			$('#editPhotoModal').modal('hide');
			$('#editPhotoFormMessage').hide();
			clearForm($('#editPhotoForm'));
		};

		function deletePhotoCancelClicked () {
			$('#deletePhotoModal').modal('hide');
			$('#deletePhotoFormMessage').hide();
			clearForm($('#deletePhotoForm'));
		};

		function deletePhotoDeleteClicked () {
			$('#deletePhotoForm').submit();
		};


        //generic showResponse and clearForm functions

        function showResponse(responseText, statusText, xhr, $form)  {
            if (responseText.substring(0, 6) == "ERROR:") {
                $form.find('.serverFeedback').removeClass('alert-success');
                $form.find('.serverFeedback').addClass('alert-error');
            }else{
                $form.find('.serverFeedback').removeClass('alert-error');
                $form.find('.serverFeedback').addClass('alert-success');
            }

            $form.find('.serverFeedback').show();
            setTimeout(function(){
                                    //only hide the modal and refresh the table/data if it's not an error message
                                    if (responseText.substring(0, 6) != "ERROR:") {
                                        $form.closest('.modal').modal('hide');
                                        $form.find('.serverFeedback').hide();
                                        clearForm($form);

                                        //update the appropriate form
                                        formID = $form.attr('id');
                                        if (formID=="createArtistForm" || formID=="editArtistForm" || formID=="deleteArtistForm"){
                                            $('#artistTableBody').load('/admin/artists/refresh');
                                        }else if (formID=="createCategoryForm" || formID=="editCategoryForm" || formID=="deleteCategoryForm"){
                                            $('#categoryTableBody').load('/admin/categories/refresh');
                                        }else if (formID=="uploadArtForm" || formID=="editArtForm" || formID=="deleteArtForm") {
                                            $('#artTableBody').load('/admin/art/refresh');
                                        }else if (formID=="editPhotoForm" || formID=="deletePhotoForm") {
                                            $('#managePhotosThumbnails').load('/admin/photos/refresh');
                                        }
                                    }//end if

                                 }, 3000);
        }

		function clearForm (form) {
		    form[0].reset();
		    formID = form.attr('id');
		    if (formID=="uploadArtForm"){
		        $("#upload-file-info").html("");
		    }
		};


    //pass parameters to modals

        //Art modals

		$(document).on("click", ".open-deleteArtModal", function () {
             var myDeleteArtID = $(this).data('id');
             $("#deleteArtKey").val(myDeleteArtID);
        });

        function fillEditArtModalDefaults(key, artist, categories, name, price, itemNumber, width, height, depth, weight, productDescription, colors, mediums, masterArtNum, photoName){
            $("#editArtKey").val(key)
            $("#editArtist").val(artist)
            $("#editCategories").val(categories)
            $("#editName").val(name)
            $("#editPrice").val(price)
			$("#editItemNumber").val(itemNumber)
			$("#editWidth").val(width)
			$("#editHeight").val(height)
			$("#editDepth").val(depth)
			$("#editWeight").val(weight)
			$("#editProductDescription").val(productDescription)
			$("#editColors").val(colors)
			$("#editMediums").val(mediums)
			$("#editMasterArtNum").val(masterArtNum)
			$("#editProductPhotoName").val(photoName)
        }


        //Artist modals

		$(document).on("click", ".open-deleteArtistModal", function () {
             var myDeleteArtistID = $(this).data('id');
             $("#deleteArtistKey").val(myDeleteArtistID);
        });

        function fillEditModalDefaults(key, firstName, lastName, biography, photoName){
            biography = biography.replace(/\r?\n/g, "<br />");
            $("#editArtistKey").val(key)
            $("#editFirstName").val(firstName)
            $("#editLastName").val(lastName)
            $("#editBiography").val(biography)
            $("#editPhotoName").val(photoName)
        }


        //Category modals

		$(document).on("click", ".open-deleteCategoryModal", function () {
             var myDeleteCategoryID = $(this).data('id');
             $("#deleteCategoryKey").val(myDeleteCategoryID);
        });

        function fillCategoryEditModalDefaults(key, categoryName, photoName){
            $("#editCategoryKey").val(key)
            $("#editCategoryName").val(categoryName)
            $("#editCategoryPhotoName").val(photoName)
        }


        //Photo modals

		$(document).on("click", ".open-deletePhotoModal", function () {
             var myDeletePhotoID = $(this).data('id');
             $("#deletePhotoKey").val(myDeletePhotoID);
        });

        function fillEditPhotoModalDefaults(key, photoName){
            $("#editPhotoKey").val(key)
            $("#editPhotoName").val(photoName)
        }