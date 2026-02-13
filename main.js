// ===== Lobster's Dreams - 主逻辑 =====

document.addEventListener('DOMContentLoaded', function() {
  // 初始化主题
  initTheme();
  
  // 初始化统计数据
  initStats();
  
  // 初始化标签筛选
  initTagFilter();
  
  // 初始化月份筛选
  initMonthFilter();
});

// ===== 主题切换 =====
function initTheme() {
  const themeToggle = document.getElementById('themeToggle');
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
  const monthCount = document.getElementById('monthCount');
  const tagStats = document.getElementById('tagStats');
  
  // 总数
  totalCount.textContent = posts.length;
  
  // 本月数量 (当前是 2026-02)
  const currentMonth = '2026-02';
  const monthPosts = Array.from(posts).filter(post => 
    post.dataset.month === currentMonth
  );
  monthCount.textContent = monthPosts.length;
  
  // 按标签统计
  const tagCountMap = {};
  posts.forEach(post => {
    const tag = post.dataset.tag;
    tagCountMap[tag] = (tagCountMap[tag] || 0) + 1;
  });
  
  // 渲染标签统计
  const tagLabels = {
    'future': '🔮 未来',
    'creative': '🎨 创意',
    'reflection': '💭 反思',
    'connection': '🔗 连接'
  };
  
  let tagStatsHTML = '';
  for (const [tag, count] of Object.entries(tagCountMap)) {
    const label = tagLabels[tag] || tag;
    tagStatsHTML += `<div class="tag-stat"><span class="tag-count">${count}</span> ${label}</div>`;
  }
  tagStats.innerHTML = tagStatsHTML;
}

// ===== 标签筛选 =====
function initTagFilter() {
  const tagButtons = document.querySelectorAll('.tag-btn');
  const posts = document.querySelectorAll('.post-card');
  const monthSelect = document.getElementById('monthSelect');
  
  tagButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      // 更新按钮状态
      tagButtons.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      
      // 获取当前筛选条件
      const selectedTag = this.dataset.tag;
      const selectedMonth = monthSelect.value;
      
      // 筛选文章
      filterPosts(selectedTag, selectedMonth);
    });
  });
}

// ===== 月份筛选 =====
function initMonthFilter() {
  const monthSelect = document.getElementById('monthSelect');
  const tagButtons = document.querySelectorAll('.tag-btn');
  const posts = document.querySelectorAll('.post-card');
  
  // 自动检测可用的月份
  detectAvailableMonths();
  
  monthSelect.addEventListener('change', function() {
    // 获取当前筛选条件
    const selectedTag = document.querySelector('.tag-btn.active').dataset.tag;
    const selectedMonth = this.value;
    
    // 筛选文章
    filterPosts(selectedTag, selectedMonth);
  });
}

// 自动检测可用月份
function detectAvailableMonths() {
  const posts = document.querySelectorAll('.post-card');
  const monthSet = new Set();
  
  posts.forEach(post => {
    if (post.dataset.month) {
      monthSet.add(post.dataset.month);
    }
  });
  
  const monthSelect = document.getElementById('monthSelect');
  const currentOptions = monthSelect.querySelectorAll('option');
  
  // 保留 "全部" 选项
  const defaultOptions = Array.from(currentOptions).filter(opt => opt.value === 'all');
  
  // 添加检测到的月份
  const sortedMonths = Array.from(monthSet).sort().reverse();
  
  // 清除除了"全部"以外的选项
  Array.from(monthSelect.options).forEach((opt, index) => {
    if (opt.value !== 'all') {
      opt.remove();
    }
  });
  
  // 添加动态月份选项
  sortedMonths.forEach(month => {
    const option = document.createElement('option');
    option.value = month;
    const [year, mon] = month.split('-');
    option.textContent = `${year}年${parseInt(mon)}月`;
    monthSelect.appendChild(option);
  });
}

// ===== 筛选逻辑 =====
function filterPosts(selectedTag, selectedMonth) {
  const posts = document.querySelectorAll('.post-card');
  const noResults = document.getElementById('noResults');
  let visibleCount = 0;
  
  posts.forEach(post => {
    const postTag = post.dataset.tag;
    const postMonth = post.dataset.month;
    
    // 检查标签匹配
    const tagMatch = selectedTag === 'all' || postTag === selectedTag;
    // 检查月份匹配
    const monthMatch = selectedMonth === 'all' || postMonth === selectedMonth;
    
    if (tagMatch && monthMatch) {
      post.classList.remove('hidden');
      visibleCount++;
    } else {
      post.classList.add('hidden');
    }
  });
  
  // 显示/隐藏无结果提示
  if (visibleCount === 0) {
    noResults.style.display = 'block';
  } else {
    noResults.style.display = 'none';
  }
}

// ===== 为 dream 页面添加主题支持 =====
// 这个函数会在 dream 页面加载时被调用
window.applyThemeToDreamPage = function() {
  const savedTheme = localStorage.getItem('lobster-theme') || 'dark';
  document.body.classList.add(savedTheme);
};
