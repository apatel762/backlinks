let pages = [window.location.pathname];
let switchDirectionWindowWidth = 900;
let animationLength = 500;

function stackNote(href, level) {
  level = Number(level) || pages.length;
  href = URI(href);
  uri = URI(window.location);
  stacks = [];
  if (uri.hasQuery("stackedNotes")) {
    stacks = uri.query(true).stackedNotes;
    if (!Array.isArray(stacks)) {
      stacks = [stacks];
    }
    stacks = stacks.slice(0, level - 1);
  }
  stacks.push(href.path());
  uri.setQuery("stackedNotes", stacks);

  old_stacks = stacks.slice(0, level - 1);
  state = { stacks: old_stacks, level: level };
  window.history.pushState(state, "", uri.href());
}

function unstackNotes(level) {
  let container = document.querySelector(".ds-grid");
  let children = Array.prototype.slice.call(container.children);

  for (let i = level; i < pages.length; i++) {
    container.removeChild(children[i]);
    destroyPreviews(children[i]);
  }
  pages = pages.slice(0, level);
}

function fetchNote(href, level, animate = false) {
  level = Number(level) || pages.length;

  const request = new Request(href);
  fetch(request)
    .then((response) => response.text())
    .then((text) => {
      unstackNotes(level);
      let container = document.querySelector(".ds-grid");
      let fragment = document.createElement("template");
      fragment.innerHTML = text;
      let element = fragment.content.querySelector(".page");
      container.appendChild(element);
      pages.push(href);

      setTimeout(
        function (element, level) {
          element.dataset.level = level + 1;
          initializePreviews(element, level + 1);
          // level 2 will be really wide to cover up the blur so if we scroll
          // into view it'll take up the whole screen
          if (level + 1 !== 2) {
            element.scrollIntoView({
              behavior: 'smooth',
              block: 'center',
              inline: 'center'
            });
          }
          if (animate) {
            element.animate([{ opacity: 0 }, { opacity: 1 }], animationLength);
          }

          if (window.MathJax) {
            window.MathJax.typeset();
          }
        }.bind(null, element, level),
        10
      );

      updateLinkStatuses();
    });
}

function updateLinkStatuses() {
  let links = Array.prototype.slice.call(
    document.querySelectorAll("a[data-uuid]")
  );

  links.forEach(function (link) {
    if (pages.indexOf(link.dataset.uuid) !== -1) {
      link.classList.add("linked");
      if (link._tippy) link._tippy.disable();
    } else {
      link.classList.remove("linked");
      if (link._tippy) link._tippy.enable();
    }
  });
}

function destroyPreviews(page) {
  links = Array.prototype.slice.call(page.querySelectorAll("a[data-uuid]"));
  links.forEach(function (link) {
    if (link.hasOwnProperty("_tippy")) {
      link._tippy.destroy();
    }
  });
}

let tippyOptions = {
  allowHTML: true,
  theme: "dark",
  interactive: true,
  interactiveBorder: 10,
  delay: 500,
  touch: ["hold", 500],
  maxWidth: "none",
  inlinePositioning: false,
  placement: "right",
};

function createPreview(link, overrideOptions) {
  level = Number(link.dataset.level);

  iframe = document.createElement('iframe');
  iframe.width = "400px";
  iframe.height = "300px";
  iframe.src = link.href

  tip = tippy(
    link,
    Object.assign(
      {},
      tippyOptions,
      {
        content: iframe
      },
      overrideOptions
    )
  );
}

function initializePreviews(page, level) {
  level = level || pages.length;

  links = Array.prototype.slice.call(page.querySelectorAll("a:not(.rooter)"));

  links.forEach(async function (element) {
    var rawHref = element.getAttribute("href");
    element.dataset.level = level;

    if (
      rawHref &&
      !(
        rawHref.indexOf("http://") === 0 ||
        rawHref.indexOf("https://") === 0 ||
        rawHref.indexOf("#") === 0 ||
        rawHref.includes(".pdf") ||
        rawHref.includes(".svg")
      )
    ) {
      var prefetchLink = element.href;
      async function myFetch() {
        let response = await fetch(prefetchLink);
        let fragment = document.createElement("template");
        fragment.innerHTML = await response.text();
        let ct = response.headers.get("content-type");
        if (ct.includes("text/html")) {
          createPreview(element, {
            placement: window.innerWidth > switchDirectionWindowWidth ? "right" : "top"
          });

          element.addEventListener("click", function (e) {
            if (!e.ctrlKey && !e.metaKey) {
              // do substring on target URL to remove the leading '/'
              const currentUrl = e.view.window.location.href
              const targetUrl = new URL(element.href).pathname.substring(1)

              // no matter what happens, we don't want the default behaviour
              // of opening the page normally; we will handle it
              e.preventDefault();

              if (level >= 2 && currentUrl.includes(targetUrl)) {
                // the page we've clicked on is already open, so find it
                // and scroll to it, but only if we've got one stacked page
                // open already. If we've only got the starting window open
                // then we can safely skip all of this (hence the level >= 2)
                const url = new URL(document.URL)
                // split().join() is a hacky way of doing .replaceAll()
                // which doesn't work for some reason
                const urlsThatAreOpen = url.href
                  .split(url.origin + '/').join('')
                  .split('?').join('')
                  .split('&').join('')
                  .split('stackedNotes=%2F')
                  .filter(o => o !== "")

                if (urlsThatAreOpen.length + 1 < level) {
                  console.log('something went wrong, we should be scrolling but we are not')
                  stackNote(element.href, this.dataset.level);
                  fetchNote(element.href, this.dataset.level, (animate = true));
                }
                else {
                  // need index, so can't use .forEach loop
                  for (let i = 0; i < urlsThatAreOpen.length; i++) {
                    const openUrl = urlsThatAreOpen[i]
                    if (targetUrl === openUrl) {
                      // the URL we want to go to is already open, so scroll to it
                      // index +1 because the first page isn't a stacked page
                      // index +1 because stacked page indices start at one
                      document
                        .querySelector('[data-level = "' + (i + 2) + '"]')
                        .scrollIntoView({
                          behavior: 'smooth',
                          block: 'center',
                          inline: 'center'
                        })
                    }
                  }
                }
              }
              else {
                stackNote(element.href, this.dataset.level);
                fetchNote(element.href, this.dataset.level, (animate = true));
              }
            }
          });
        };
      }
      return myFetch();
    }
  });
}

window.addEventListener("popstate", function (event) {
  // TODO: check state and pop pages if possible, rather than reloading.
  window.location = window.location; // this reloads the page.
});

window.onload = function () {
  initializePreviews(document.querySelector(".page"));

  uri = URI(window.location);
  if (uri.hasQuery("stackedNotes")) {
    stacks = uri.query(true).stackedNotes;
    if (!Array.isArray(stacks)) {
      stacks = [stacks];
    }
    for (let i = 1; i <= stacks.length; i++) {
      fetchNote(stacks[i - 1], i);
    }
  }
};
