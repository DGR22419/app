// Initialize DataTable on document ready
$(document).ready(function() {
    $('#resultsTable').DataTable({
        paging: true,
        searching: true,
        ordering: true,
        info: true,
        lengthChange: true
    });
});

// Fetch dynamic quiz details from Django context
// const quizDetails = [
//     'Quiz Title: ' + "{{ quiz.title }}",
//     'Date: ' + "{{ quiz.created_at }}",
//     'Room Code: ' + "{{ quiz.code }}",
//     'Total Questions: ' + "{{ total_questions }}"
// ];
const quizDetails = [
    'Quiz Title: ' + "{{ quiz.title|escapejs }}",
    'Date: ' + "{{ quiz.created_at|escapejs }}",
    'Room Code: ' + "{{ quiz.code|escapejs }}",
    'Total Questions: ' + "{{ total_questions|escapejs }}"
];

// Function to export content to PDF
function exportToPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Add Quiz Details Section
    quizDetails.forEach((detail, index) => {
        doc.setFontSize(index === 0 ? 16 : 12); // Larger font for title
        doc.text(detail, 10, 10 + (index * 10)); // Adjust Y position dynamically
    });

    // Add Student Scores Table
    doc.autoTable({
        html: '#resultsTable',
        startY: 55,
        styles: { fontSize: 10 },
        headStyles: { fillColor: [22, 160, 133] },
        theme: 'striped'
    });

    // Save the PDF document
    doc.save('quiz_results.pdf');
}

// Function to export content to CSV
function exportToCSV() {
    const table = document.getElementById("resultsTable");
    const rows = Array.from(table.rows);

    // Add Quiz Details to CSV Content
    let csvContent = quizDetails.map(detail => escapeCSVValue(detail)).join('\n') + '\n\n';

    // Convert Table Data to CSV Format
    csvContent += rows.map(row => Array.from(row.cells).map(cell => escapeCSVValue(cell.innerText)).join(",")).join('\n');

    // Create a downloadable CSV file
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "quiz_results.csv";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Utility function to escape CSV values
function escapeCSVValue(value) {
    return '"' + value.replace(/"/g, '""') + '"';
}