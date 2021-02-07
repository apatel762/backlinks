var idx,
    jsonIndex,
    resultsList,
    searchBox;

/**
 * Execute a callback when the document has finished loading
 * @param {Function} fn the callback to execute
 */
function whenDocumentIsReady(fn) {
    if (document.readyState != 'loading') {
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}

/**
 * Remove everything from a list
 * @param {Element} listElement An ordered list or unordered list element
 */
function empty(listElement) {
    while (listElement.firstChild) {
        listElement.removeChild(listElement.firstChild);
    }
}

function getResultsListElement() {
    return document.querySelector('#results');
}

function getSearchBox() {
    return document.querySelector('#search')
}

function createLink(href, display) {
    var a = document.createElement('a');
    a.href = href;
    a.innerHTML = display;
    return a;
}

function exists(o) {
    return o !== undefined && o !== null;
}

function renderResults(results) {
    if (!results.length) {
        return;
    }

    // get first ten results and put them into the results list
    results.slice(0, 10).forEach(result => {
        var entry = document.createElement('li');
        entry.append(createLink(result.href, result.title));
        resultsList.appendChild(entry);
    });
}

function searchPosts(query) {
    const fuzzyQuery = query.split(' ').join('~2');
    return idx
        .search(fuzzyQuery)
        .map(item => jsonIndex.find((el) => item.ref === el.href));
}

function handleSearchBoxKeyPress(keyUpEvent) {
    // with each key pressed, we should re-populate the search results
    empty(resultsList);

    // trigger search when at least two chars provided.
    var query = searchBox.value;
    if (query.length < 2) {
        return;
    }

    renderResults(searchPosts(query));
}

function populateLunrIndex(json) {
    return lunr(function () {
        // tell lunr to expect an 'href' and 'title' in each of the elements
        // in the JSON
        this.ref('href')
        this.field("title", {
            boost: 10
        });

        // cache the complete JSON index
        jsonIndex = json;

        // load the JSON elements into lunr one-by-one
        json.forEach(function (element) {
            try {
                this.add(element)
            } catch (e) {
                // no-op; swallow exception
            }
        }, this);
    });
}

function prepIndex(jsonFilePath) {
    fetch(jsonFilePath)
        .then(response => response.json())
        .then(json => idx = populateLunrIndex(json))
        .catch(err => alert('something went wrong getting the index.json' + err));
}

prepIndex('/js/index.json');

whenDocumentIsReady(function () {
    // cache these two elements
    resultsList = getResultsListElement();
    searchBox = getSearchBox();

    if (exists(resultsList) && exists(searchBox)) {
        getSearchBox().addEventListener("keyup", e => handleSearchBoxKeyPress(e));
    }
    else {
        alert('one of: #search or #results isnt in the DOM, no search available')
    }

});