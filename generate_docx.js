const fs = require('fs');
const htmlToDocx = require('html-to-docx');
const cheerio = require('cheerio');

(async () => {
    try {
        const html = fs.readFileSync('index.html', 'utf8');
        const $ = cheerio.load(html);
        
        // Target cleanup
        $('script, style, svg, iframe, nav, footer, img').remove();
        
        // Remove visually hidden or purely decorative elements if needed
        $('.tag').css('font-weight', 'bold');
        
        // Mark each page section with a clear heading
        $('.page').each((i, page) => {
            const pageId = $(page).attr('id') || `section-${i}`;
            const title = pageId.replace('pg-', '').toUpperCase();
            $(page).prepend(`<h1>========== SECTION: ${title} ==========</h1><br/>`);
            $(page).append('<br/><br/>');
        });
        
        // Add a master title
        $('body').prepend('<h1>Lee Hydraulics & Fasteners - Full Website Content</h1><br/>');

        // Extract the simplified body HTML
        const cleanHtml = $('body').html();
        
        // Generate buffer
        const fileBuffer = await htmlToDocx(cleanHtml, null, {
            table: { row: { cantSplit: true } },
            footer: true,
            pageNumber: true,
            font: 'Arial'
        });
        
        fs.writeFileSync('Website_Content.docx', fileBuffer);
        console.log('Website_Content.docx generated successfully!');
    } catch (e) {
        console.error('Error generating document:', e);
    }
})();
