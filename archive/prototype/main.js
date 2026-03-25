// ===== Lobster Mind - 主逻辑 =====

document.addEventListener('DOMContentLoaded', function() {
  // 初始化主题
  initTheme();
  
  // 初始化统计数据
  initStats();
  
  // 初始化板块筛选
  initSectionFilter();
});

// ===== 主题切换 =====
function initTheme() {
  const themeToggle = document.getElementById('themeToggle');
  if (!themeToggle) return;
  
  const themeIcon = themeToggle.querySelector('.theme-icon');
  
  // 从 localStorage 读取主题偏好
  const savedTheme = localStorage.getItem('lobster-theme') || 'dark';
  document.body.classList.add(savedTheme);
  updateThemeIcon(savedTheme);
  
  // 点击切换主题
  themeToggle.addEventListener('click', function() {
    const currentTheme = document.body.classList.contains('dark') ? 'dark' : 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.body.classList.remove(currentTheme);
    document.body.classList.add(newTheme);
    
    // 保存到 localStorage
    localStorage.setItem('lobster-theme', newTheme);
    
    // 更新图标
    updateThemeIcon(newTheme);
  });
  
  // 更新主题图标
  function updateThemeIcon(theme) {
    themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
  }
}

// ===== 统计信息 =====
function initStats() {
  const posts = document.querySelectorAll('.post-card');
  const totalCount = document.getElementById('totalCount');
  
  if (!totalCount) return;
  
  // 总数
  totalCount.textContent = posts.length;
  
  // 按板块统计
  const sectionCountMap = {};
  posts.forEach(post => {
    const section = post.dataset.section;
    if (section) {
      sectionCountMap[section] = (sectionCountMap[section] || 0) + 1;
    }
  });
}

// ===== 板块筛选 =====
function initSectionFilter() {
  const sectionButtons = document.querySelectorAll('#sectionFilter .tag-btn');
  if (sectionButtons.length === 0) return;
  
  const posts = document.querySelectorAll('.post-card');
  
  sectionButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      // 更新按钮状态
      sectionButtons.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      
      // 获取选中的板块
      const selectedSection = this.dataset.filter;
      
      // 筛选文章
      filterPostsBySection(selectedSection);
    });
  });
}

// ===== 筛选逻辑 =====
function filterPostsBySection(selectedSection) {
  const posts = document.querySelectorAll('.post-card');
  const noResults = document.getElementById('noResults');
  let visibleCount = 0;
  
  posts.forEach(post => {
    const postSection = post.dataset.section;
    
    // 检查板块匹配
    const sectionMatch = selectedSection === 'all' || postSection === selectedSection;
    
    if (sectionMatch) {
      post.classList.remove('hidden');
      visibleCount++;
    } else {
      post.classList.add('hidden');
    }
  });
  
  // 显示/隐藏无结果提示
  if (noResults) {
    if (visibleCount === 0) {
      noResults.style.display = 'block';
    } else {
      noResults.style.display = 'none';
    }
  }
}

// ===== 为文章页添加主题支持 =====
window.applyThemeToPage = function() {
  const savedTheme = localStorage.getItem('lobster-theme') || 'dark';
  document.body.classList.add(savedTheme);
};
