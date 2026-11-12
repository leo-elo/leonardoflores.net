(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {

    // ── Accordion for sidebar unit headers ──────────────────────────────
    document.querySelectorAll('.nav-term-header').forEach(function (header) {
      var items = [];
      var el = header.nextElementSibling;
      while (el && !el.classList.contains('nav-term-header')) {
        items.push(el);
        el = el.nextElementSibling;
      }
      if (!items.length) return;

      header.classList.add('accordion-open');

      header.addEventListener('click', function () {
        var open = header.classList.toggle('accordion-open');
        items.forEach(function (item) {
          item.classList.toggle('accordion-hidden', !open);
        });
      });
    });

    // ── Desktop sidebar collapse / expand ───────────────────────────────
    var sidebarHeader = document.querySelector('.sidebar-header');
    if (sidebarHeader) {
      var collapseBtn = document.createElement('button');
      collapseBtn.className = 'sidebar-collapse-btn';
      collapseBtn.setAttribute('aria-label', 'Collapse sidebar');
      collapseBtn.textContent = '«'; // «

      sidebarHeader.appendChild(collapseBtn);

      var expandBtn = document.createElement('button');
      expandBtn.className = 'sidebar-expand-btn';
      expandBtn.setAttribute('aria-label', 'Expand sidebar');
      expandBtn.textContent = '»'; // »
      document.body.appendChild(expandBtn);

      collapseBtn.addEventListener('click', function () {
        document.body.classList.add('sidebar-collapsed');
      });

      expandBtn.addEventListener('click', function () {
        document.body.classList.remove('sidebar-collapsed');
      });
    }

    // ── Banner image lightbox ───────────────────────────────────────────
    var banner = document.querySelector('.banner');
    if (banner) {
      var styleAttr = banner.getAttribute('style') || '';
      var match = styleAttr.match(/url\(['"]?([^'")\s]+)['"]?\)/);
      if (match) {
        var imgUrl = match[1];

        var lb = document.createElement('div');
        lb.className = 'banner-lightbox';

        var lbImg = document.createElement('img');
        lbImg.className = 'banner-lightbox-img';
        lbImg.src = imgUrl;
        lbImg.alt = 'Header image';

        var lbClose = document.createElement('button');
        lbClose.className = 'banner-lightbox-close';
        lbClose.setAttribute('aria-label', 'Close');
        lbClose.textContent = '×'; // ×

        lb.appendChild(lbImg);
        lb.appendChild(lbClose);
        document.body.appendChild(lb);

        banner.addEventListener('click', function () {
          lb.classList.add('active');
        });

        lb.addEventListener('click', function (e) {
          if (e.target !== lbImg) {
            lb.classList.remove('active');
          }
        });

        document.addEventListener('keydown', function (e) {
          if (e.key === 'Escape' && lb.classList.contains('active')) {
            lb.classList.remove('active');
          }
        });
      }
    }

  });
}());
