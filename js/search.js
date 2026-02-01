/**
 * Client-side search functionality for Leonardo Flores static site
 */

let postsData = [];
let searchTimeout = null;

// Load posts data
async function loadPostsData() {
    try {
        const response = await fetch('posts-data.json');
        postsData = await response.json();
    } catch (error) {
        console.error('Error loading posts data:', error);
    }
}

// Search function
function searchPosts(query) {
    if (!query || query.length < 2) {
        return [];
    }

    const lowerQuery = query.toLowerCase();
    const results = [];

    for (const post of postsData) {
        const title = (post.title || '').toLowerCase();
        const excerpt = (post.excerpt || '').toLowerCase();
        const category = (post.category || '').toLowerCase();

        // Score matches
        let score = 0;
        if (title.includes(lowerQuery)) score += 10;
        if (excerpt.includes(lowerQuery)) score += 5;
        if (category.includes(lowerQuery)) score += 3;

        if (score > 0) {
            results.push({ ...post, score });
        }
    }

    // Sort by score (highest first)
    results.sort((a, b) => b.score - a.score);

    return results.slice(0, 10); // Return top 10 results
}

// Display search results
function displaySearchResults(results) {
    const resultsContainer = document.getElementById('searchResults');

    if (results.length === 0) {
        resultsContainer.innerHTML = '<div class="search-no-results">No results found</div>';
        resultsContainer.classList.remove('hidden');
        return;
    }

    const resultsHTML = results.map(post => `
        <a href="${post.url}" class="search-result-item">
            <div class="search-result-title">${post.title}</div>
            <div class="search-result-excerpt">${post.excerpt.substring(0, 100)}...</div>
            ${post.date ? `<div class="search-result-date">${post.date}</div>` : ''}
        </a>
    `).join('');

    resultsContainer.innerHTML = resultsHTML;
    resultsContainer.classList.remove('hidden');
}

// Hide search results
function hideSearchResults() {
    const resultsContainer = document.getElementById('searchResults');
    resultsContainer.classList.add('hidden');
}

// Handle search input
function handleSearchInput(event) {
    const query = event.target.value.trim();

    // Clear previous timeout
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }

    // If query is empty, hide results
    if (!query) {
        hideSearchResults();
        return;
    }

    // Debounce search
    searchTimeout = setTimeout(() => {
        const results = searchPosts(query);
        displaySearchResults(results);
    }, 300);
}

// Initialize search
function initSearch() {
    const searchInput = document.getElementById('searchInput');

    if (!searchInput) {
        return;
    }

    // Load posts data
    loadPostsData();

    // Add event listeners
    searchInput.addEventListener('input', handleSearchInput);

    // Close search results when clicking outside
    document.addEventListener('click', (event) => {
        const searchContainer = event.target.closest('.search-container');
        if (!searchContainer) {
            hideSearchResults();
        }
    });

    // Prevent closing when clicking inside search container
    searchInput.addEventListener('click', (event) => {
        event.stopPropagation();
        // Re-show results if there's a query
        if (searchInput.value.trim()) {
            const results = searchPosts(searchInput.value.trim());
            displaySearchResults(results);
        }
    });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSearch);
} else {
    initSearch();
}
