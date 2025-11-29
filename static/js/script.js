document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initNavigation();
    initScrollEffects();
    initAnimations();
    initTabs();
    initModals();

    console.log('%c🎓 Abruisdev - Online Dasturlash Kurslari', 'font-size: 20px; font-weight: bold; color: #4F46E5;');
});

window.addEventListener('load', function() {
    document.body.style.opacity = '0';
    setTimeout(function() {
        document.body.style.transition = 'opacity 0.5s ease';
        document.body.style.opacity = '1';
    }, 100);
});
//function initTheme() {
//    const themeToggle = document.getElementById('themeToggle');
//    const savedTheme = localStorage.getItem('theme');
//    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
//
//    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
//        applyTheme('dark');
//    } else {
//        applyTheme('light');
//    }
//
//    if (themeToggle) {
//        themeToggle.addEventListener('click', function(e) {
//            e.preventDefault();
//            const currentTheme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
//            applyTheme(currentTheme === 'light' ? 'dark' : 'light');
//        });
//    }
//}
function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const savedTheme = localStorage.getItem('theme');

    // YANGI LOGIKA:
    // Agar oldin hech qachon tanlanmagan bo‘lsa → majburan 'dark' qilamiz
    if (!savedTheme) {
        applyTheme('dark');
    } else {
        applyTheme(savedTheme);
    }

    // Tugma bosilganda almashsin
    if (themeToggle) {
        themeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            const currentTheme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
            applyTheme(currentTheme === 'light' ? 'dark' : 'light');
        });
    }
}
function applyTheme(theme) {
    const themeIcon = document.getElementById('themeIcon');
    const themeToggle = document.getElementById('themeToggle');

    if (theme === 'dark') {
        document.body.classList.add('dark-mode');
        if (themeIcon) {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        }
    } else {
        document.body.classList.remove('dark-mode');
        if (themeIcon) {
            themeIcon.classList.add('fa-moon');
            themeIcon.classList.remove('fa-sun');
        }
    }
    localStorage.setItem('theme', theme);
}

function toggleDarkMode() {
    const currentTheme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    applyTheme(currentTheme === 'light' ? 'dark' : 'light');
}

function initNavigation() {
    const navbar = document.getElementById('navbar') || document.querySelector('.navbar');
    const navbarToggle = document.getElementById('navbarToggle') || document.querySelector('.navbar-toggle');
    const navbarMenu = document.getElementById('navbarMenu') || document.querySelector('.navbar-menu');

    if (navbarToggle && navbarMenu) {
        navbarToggle.addEventListener('click', function() {
            navbarToggle.classList.toggle('active');
            navbarMenu.classList.toggle('active');
        });
    }

    document.addEventListener('click', function(e) {
        if (navbarToggle && navbarMenu) {
            if (!navbarToggle.contains(e.target) && !navbarMenu.contains(e.target)) {
                navbarToggle.classList.remove('active');
                navbarMenu.classList.remove('active');
            }
        }
    });

    window.addEventListener('scroll', function() {
        if (navbar) {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        }
    });
}

function initScrollEffects() {
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                const navbarHeight = document.querySelector('.navbar')?.offsetHeight || 70;
                window.scrollTo({
                    top: target.offsetTop - navbarHeight - 20,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Scroll to top button
    const scrollTopBtn = document.getElementById('scrollTop');
    if (scrollTopBtn) {
        window.addEventListener('scroll', function() {
            scrollTopBtn.classList.toggle('visible', window.scrollY > 500);
        });

        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
}

function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.course-card');
    animatedElements.forEach(function(el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const tabName = btn.dataset.tab || btn.getAttribute('onclick')?.match(/switchTab\('([^']+)'/)?.[1];
            if (tabName) {
                switchTab(tabName, btn);
            }
        });
    });
}

function switchTab(tabName, clickedBtn) {
    document.querySelectorAll('.tab-content').forEach(function(tab) {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(function(btn) {
        btn.classList.remove('active');
    });

    const tabContent = document.getElementById(tabName);
    if (tabContent) tabContent.classList.add('active');
    if (clickedBtn) clickedBtn.classList.add('active');
}

function initModals() {
    const telegramModal = document.getElementById('telegramModal');
    if (telegramModal) {
        telegramModal.addEventListener('click', function(e) {
            if (e.target === this) closeTelegramModal();
        });
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeTelegramModal();
    });
}

function openTelegramModal() {
    const telegramModal = document.getElementById('telegramModal');
    if (telegramModal) telegramModal.style.display = 'flex';
}

function closeTelegramModal() {
    const telegramModal = document.getElementById('telegramModal');
    if (telegramModal) telegramModal.style.display = 'none';
}

function goToCourse(id) {
    const baseUrl = window.COURSE_DETAIL_URL || '/course/';
    window.location.href = baseUrl + id + '/';
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}

window.formatNumber = formatNumber;
window.goToCourse = goToCourse;
window.switchTab = switchTab;
window.openTelegramModal = openTelegramModal;
window.closeTelegramModal = closeTelegramModal;
window.toggleDarkMode = toggleDarkMode;