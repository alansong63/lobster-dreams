const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function generatePDF() {
  console.log('启动浏览器...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu'
    ]
  });

  try {
    const page = await browser.newPage();
    
    console.log('访问 Notion 博客...');
    await page.goto('https://www.notion.com/blog/steam-steel-and-infinite-minds-ai', {
      waitUntil: 'networkidle2',
      timeout: 60000
    });
    
    // 等待图片加载
    console.log('等待图片加载...');
    await page.evaluate(() => {
      const images = document.querySelectorAll('img');
      images.forEach(img => {
        if (!img.complete) {
          img.onload = () => console.log('图片加载完成');
        }
      });
    });
    
    // 等待一下确保图片加载完成
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    console.log('生成 PDF...');
    const pdf = await page.pdf({
      path: '/home/ubuntu/.openclaw/workspace/steam-steel-infinite-minds-en-full.pdf',
      format: 'A4',
      printBackground: true,
      margin: {
        top: '20px',
        right: '20px',
        bottom: '20px',
        left: '20px'
      }
    });
    
    console.log(`PDF 生成成功！大小: ${pdf.length} bytes`);
    console.log('文件保存在: /home/ubuntu/.openclaw/workspace/steam-steel-infinite-minds-en-full.pdf');
    
  } catch (error) {
    console.error('生成 PDF 时出错:', error.message);
  } finally {
    await browser.close();
  }
}

generatePDF().catch(console.error);
