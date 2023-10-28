const detailModal = document.getElementById("detail-modal");
var detailModalChanged = false;

var sortOption = 'alphabetical'
var filterOption = 'all'
var layoutOption = 'grid'
var cachedLibrary = null;
var sortedCachedLibrary = null;

async function getLibrary() {
    return fetch(url_get_library).then((res) => res.json())
}

async function applySortAndFilters() {
    let sortedJson = JSON.parse(JSON.stringify(cachedLibrary));
    let sortDirection = sortDirectionToggle.getAttribute('data-sort-direction')
    
    if (sortOption === 'alphabetical') {
        sortedJson = sortedJson.sort(function(a,b){
            let x = a["book_data"].title.toLowerCase();
            let y = b["book_data"].title.toLowerCase();

            //compare title
            if(x>y){return sortDirection*1;} 
            if(x<y){return sortDirection*-1;}
            return 0;
        });
    } else if (sortOption === 'recent') {
        sortedJson = sortedJson.sort(function(a,b){
            let x = a["library_data"].id;
            let y = b["library_data"].id;

            //compare title
            if(x<y){return sortDirection*1;} 
            if(x>y){return sortDirection*-1;}
            return 0;
        });
    } else if (sortOption === 'tracking') {
        sortedJson = sortedJson.sort(function(a,b){
            let x = a["library_data"].tracking_status;
            let y = b["library_data"].tracking_status;

            //compare title
            if(x<y){return sortDirection*1;} 
            if(x>y){return sortDirection*-1;}
            return 0;
        });
    }

    // filtering...
    if (filterOption === 'favorites') {
        sortedJson = sortedJson.filter(obj => obj["library_data"].is_favorited == true);
    } else if (filterOption === 'finished') {
        sortedJson = sortedJson.filter(obj => obj["library_data"].tracking_status == 1);
    } else if (filterOption === 'reviewed') {
        sortedJson = sortedJson.filter(obj => obj["library_data"].is_reviewed == true);
    }
    return sortedJson
}

function renderTags() {
    document.querySelectorAll('[data-tag-tracking-status]').forEach(tag => {
        let tag_text = tag.getAttribute('data-tag-tracking-status');
        if (tag_text == 0) {
            tag_text = "untracked";
        } else if (tag_text == 1) {
            tag_text = "finished reading";
        } else if (tag_text == 2) {
            tag_text = "currently reading";
        } else if (tag_text == 3) {
            tag_text = "on hold";
        } else if (tag_text == 4) {
            tag_text = "planning to read";
        } else if (tag_text == 5) {
            tag_text = "dropped";
        }
        tag.textContent = tag_text;
    })
}

async function redrawLibrary() {
    let htmlString = ``;
    var counter = 0;
    
    sortedCachedLibrary.forEach((library_item) => {
        const book_data = library_item["book_data"];
        const library_data = library_item["library_data"];
        console.log(book_data)
        counter++;
        if (layoutOption == 'grid') {
            htmlString += 
            `<div class="g-col">
                <div class="book-card p-0 d-flex flex-column justify-content-center m-0 gap-2" data-lib-book-id=${book_data.id}>
                    <img src=${book_data.thumbnail} class="img-fluid rounded border border-1 shadow-sm" alt="${book_data.title} by ${book_data.authors}" data-bs-toggle="modal" data-bs-target="#detail-modal">                     
                    <span class="text-center fst-italic">${book_data.title}</span>
                </div>
            </div>
            \n`
        } else if (layoutOption == 'list') {
            htmlString += 
            `<div class="g-col">
                <div class="book-card card mb-3 shadow-sm bg-body-tertiary" data-lib-book-id=${book_data.id}>
                    <div class="row g-0">
                        <div class="col-1 col-lg-2">
                            <img src=${book_data.thumbnail} class="h-auto img-fluid rounded-start" alt="...">
                        </div>
                        <div class="col-11 col-lg-10">
                            <div class="card-body d-flex flex-row">
                                <div class="me-auto d-flex flex-column">
                                    <h5 class="card-title">${book_data.title}</h5>
                                    <span class="card-text">by ${book_data.authors}</span>
                                    <div class="mt-2">
                                        <span class="badge bg-secondary" data-tag-tracking-status=${library_data.tracking_status}></span>
                                    </div>
                                </div>
                                <div>
                                    <button type="button" class="btn detail-modal-trigger" data-bs-toggle="modal" data-bs-title="Open detail" data-bs-trigger="hover" data-bs-target="#detail-modal">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-three-dots-vertical" viewBox="0 0 16 16">
                                            <path d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            \n`
        }
    })

    const library_div = document.getElementById("library-books")
    library_div.className = ""
    if (htmlString === ``) {
        htmlString = `
        <span class="fst-italic text-secondary-emphasis">Your library has no books fitting that filter :(</span>\n
        `
        library_div.classList.add("d-flex", "justify-content-center", "my-4", "mx-sm-0")
    } else {
        if (layoutOption == 'grid') {
            library_div.classList.add("row", "row-cols-2", "row-cols-lg-6", "row-cols-md-6", "row-cols-sm-4", "my-4", "mx-sm-0", "justify-content-center", "row-gap-3")
        } else {
            library_div.classList.add("row", "row-cols-lg-2", "row-cols-sm-1", "my-4", "mx-sm-0")
        }
    }
    
    library_div.innerHTML = htmlString
    renderTags();
    await connectListeners();
    console.log('counter: ' + counter)
}

async function updateDetailModal(id) {
    const thumbnailImg = document.getElementById("detail-thumbnail")
    const titleLabel = document.getElementById("detail-title-label")
    const authorLabel = document.getElementById("detail-authors-label")
    const bookLink = document.getElementById("detail-book-link")
    const reviewLink = document.getElementById("detail-review-link")

    const item_data = cachedLibrary.filter(obj => obj["book_data"].id == id)[0];

    detailModal.setAttribute("data-lib-book-id", id)
    thumbnailImg.src = item_data["book_data"].thumbnail;
    thumbnailImg.alt = "Cover of " + item_data["book_data"].title + " by " + item_data["book_data"].authors;
    titleLabel.textContent = item_data["book_data"].title;
    authorLabel.textContent = "by " + item_data["book_data"].authors;
    bookLink.setAttribute('href', url_book_details.replace(/12345/, item_data["book_data"].id));
    reviewLink.setAttribute('href', 'url_review_book.replace(/12345/, item_data["book_data"].id)');
}

async function connectListeners() {
    if (layoutOption == 'grid') {
        document.querySelectorAll('#library-books img').forEach((element) => {
            element.addEventListener("click", function(e){
                updateDetailModal(element.closest(".book-card").getAttribute("data-lib-book-id"))
            })
        })
    } else if (layoutOption == 'list') {
        // connect buttons
        document.querySelectorAll('#library-books .detail-modal-trigger').forEach((element) => {
            new bootstrap.Tooltip(element);
            element.addEventListener("click", function(e){
                updateDetailModal(element.closest(".book-card").getAttribute("data-lib-book-id"))
            })
        })
    }
}

async function refreshLibrary() {
    cachedLibrary = (await getLibrary())["library"];
    sortedCachedLibrary = await applySortAndFilters();
    await redrawLibrary();
}
refreshLibrary()

function updateSortDirectionIcon(newDirection) {
    let svg = ``;
    if (newDirection == 1) {
        svg = `
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-sort-down" viewBox="0 0 16 16">
            <path d="M3.5 2.5a.5.5 0 0 0-1 0v8.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L3.5 11.293V2.5zm3.5 1a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5zM7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1h-5zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1h-3zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1h-1z"/>
        </svg>
        `;
    } else {
        svg = `
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-sort-up" viewBox="0 0 16 16">
            <path d="M3.5 12.5a.5.5 0 0 1-1 0V3.707L1.354 4.854a.5.5 0 1 1-.708-.708l2-1.999.007-.007a.498.498 0 0 1 .7.006l2 2a.5.5 0 1 1-.707.708L3.5 3.707V12.5zm3.5-9a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5zM7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1h-5zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1h-3zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1h-1z"/>
        </svg>
        `;
    }
    document.getElementById("sort-direction-toggle").innerHTML = svg;
}

// bind sort selection
let sortSelection = document.getElementById('sort-selection')
sortSelection.addEventListener('input', async () => {
    sortOption = sortSelection.value
    sortedCachedLibrary = await applySortAndFilters();
    redrawLibrary()
});

// bind filter selection
let filterSelection = document.getElementById('filter-selection')
filterSelection.addEventListener('input', async () => {
    filterOption = filterSelection.value
    sortedCachedLibrary = await applySortAndFilters()
    redrawLibrary()
});

// bind sort direction button
let sortDirectionToggle = document.getElementById('sort-direction-toggle')
sortDirectionToggle.addEventListener('click', async () => {
    const lastDirection = sortDirectionToggle.getAttribute('data-sort-direction')
    sortDirectionToggle.setAttribute("data-sort-direction", (lastDirection == 1 ? -1 : 1))

    sortedCachedLibrary = await applySortAndFilters()
    redrawLibrary()
    updateSortDirectionIcon(sortDirectionToggle.getAttribute('data-sort-direction'));
})

// bind list/grid display toggle
let listToggle = document.getElementById('display-list-toggle')
listToggle.addEventListener('click', async () => {
    if (layoutOption != 'list') {
        layoutOption = 'list'
        redrawLibrary();
        updateGridToggleIcon();
        updateListToggleIcon();
    }
})
let gridToggle = document.getElementById('display-grid-toggle')
gridToggle.addEventListener('click', async () => {
    if (layoutOption != 'grid') {
        layoutOption = 'grid'
        redrawLibrary()
        updateGridToggleIcon();
        updateListToggleIcon();
    }
})

function updateGridToggleIcon() {
    let svg = ``;
    if (layoutOption == 'grid') {
        gridToggle.classList.add("active");
        svg = `
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-grid-3x2-gap-fill" viewBox="0 0 16 16">
            <path d="M1 4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V4zm5 0a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4zm5 0a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V4zM1 9a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V9zm5 0a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V9zm5 0a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V9z"/>
        </svg>
        `;
    } else {
        gridToggle.classList.remove("active");
        svg = `
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-grid-3x2" viewBox="0 0 16 16">
            <path d="M0 3.5A1.5 1.5 0 0 1 1.5 2h13A1.5 1.5 0 0 1 16 3.5v8a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 0 11.5v-8zM1.5 3a.5.5 0 0 0-.5.5V7h4V3H1.5zM5 8H1v3.5a.5.5 0 0 0 .5.5H5V8zm1 0v4h4V8H6zm4-1V3H6v4h4zm1 1v4h3.5a.5.5 0 0 0 .5-.5V8h-4zm0-1h4V3.5a.5.5 0 0 0-.5-.5H11v4z"/>
        </svg>
        `;
    }
    gridToggle.innerHTML = svg;
}
function updateListToggleIcon() {
    if (layoutOption == 'list') {
        listToggle.classList.add("active");
    } else {
        listToggle.classList.remove("active");
    }
}
updateGridToggleIcon();

// refresh library button
document.getElementById('refresh-library').addEventListener('click', refreshLibrary)

// tooltips
let tooltipelements = document.querySelectorAll("[data-bs-toggle='tooltip']");
tooltipelements.forEach((el) => {
    new bootstrap.Tooltip(el);
});

// modal stuff
document.getElementById('tracking-status-selection').addEventListener('input', async () => {
    detailModalChanged = true;
    // change status it
})
document.getElementById('lib_button_remove').addEventListener('click', async () => {
    detailModalChanged = true;
    // remove it
})
document.getElementById('lib_button_fav').addEventListener('click', async () => {
    detailModalChanged = true;
    // favorite it
})
detailModal.addEventListener('hide.bs.modal', async function(e) {
    // check if theres any change
    if (detailModalChanged === true) {
        await refreshLibrary();
    }
    detailModalChanged = false;
    console.log("boop")
})