document.addEventListener("DOMContentLoaded", () => {
    // UI Elements
    const openModalBtn = document.getElementById("open-modal-btn");
    const heroStartBtn = document.getElementById("hero-start-btn");
    const closeModalBtn = document.getElementById("close-modal-btn");
    const cancelModalBtn = document.getElementById("cancel-modal-btn");
    const ideaModal = document.getElementById("idea-modal");
    const ideaForm = document.getElementById("idea-form");

    const welcomeSection = document.getElementById("welcome-section");
    const testRunnerSection = document.getElementById("test-runner-section");
    
    const displayTitle = document.getElementById("display-idea-title");
    const displayTarget = document.getElementById("display-idea-target");
    const statusSpinner = document.getElementById("status-spinner");
    const statusText = document.getElementById("status-text");

    const copyReportBtn = document.getElementById("copy-report-btn");
    const downloadPdfBtn = document.getElementById("download-pdf-btn");
    const downloadMdBtn = document.getElementById("download-md-btn");

    const qaQuestionInput = document.getElementById("qa-question-input");
    const sendQuestionBtn = document.getElementById("send-question-btn");
    const qaMessagesList = document.getElementById("qa-messages-list");

    let currentJobId = null;
    let pollInterval = null;
    let radarChart = null;
    let latestReportMarkdown = "";

    // Helper: Safe Markdown Sanitation (XSS Defense)
    function renderSafeMarkdown(rawMarkdown) {
        if (!rawMarkdown) return "";
        const html = marked.parse(rawMarkdown);
        if (window.DOMPurify) {
            return DOMPurify.sanitize(html);
        }
        return html;
    }

    // Modal Handlers
    const openModal = () => ideaModal.classList.remove("hidden");
    const closeModal = () => ideaModal.classList.add("hidden");

    if (openModalBtn) openModalBtn.addEventListener("click", openModal);
    if (heroStartBtn) heroStartBtn.addEventListener("click", openModal);
    if (closeModalBtn) closeModalBtn.addEventListener("click", closeModal);
    if (cancelModalBtn) cancelModalBtn.addEventListener("click", closeModal);

    // Close modal on overlay click
    ideaModal.addEventListener("click", (e) => {
        if (e.target === ideaModal) closeModal();
    });

    // Agent Accordion Toggles
    for (let i = 0; i < 4; i++) {
        const cardHeader = document.querySelector(`#agent-card-${i} .agent-card-header`);
        const cardBody = document.getElementById(`agent-body-${i}`);
        if (cardHeader && cardBody) {
            cardHeader.addEventListener("click", () => {
                cardBody.classList.toggle("hidden");
            });
        }
    }

    // Form Submission
    ideaForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const title = document.getElementById("input-title").value.trim();
        const description = document.getElementById("input-description").value.trim();
        const targetAudience = document.getElementById("input-target").value.trim();

        if (!title || !description) return;

        closeModal();

        // Show test runner view
        welcomeSection.classList.add("hidden");
        testRunnerSection.classList.remove("hidden");

        displayTitle.textContent = title;
        displayTarget.innerHTML = `<i class="fa-solid fa-bullseye"></i> Hedef Kitle: ${targetAudience || 'Belirtilmedi'}`;

        resetAgentCards();

        try {
            statusText.textContent = "Ajanlar Başlatılıyor...";
            statusSpinner.classList.remove("hidden");

            const res = await fetch("/api/evaluate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    title: title,
                    description: description,
                    target_audience: targetAudience
                })
            });

            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || "İstek başarısız oldu.");

            currentJobId = data.job_id;
            startPollingStatus(currentJobId);

        } catch (err) {
            statusSpinner.classList.add("hidden");
            statusText.textContent = `Hata: ${err.message}`;
            alert(`Test başlatılamadı: ${err.message}`);
        }
    });

    // Reset Agent Cards UI
    function resetAgentCards() {
        for (let i = 0; i < 4; i++) {
            const badge = document.getElementById(`status-badge-${i}`);
            const text = document.getElementById(`agent-text-${i}`);
            const body = document.getElementById(`agent-body-${i}`);
            
            if (badge) {
                badge.className = "agent-status-badge badge-pending";
                badge.textContent = "Bekliyor";
            }
            if (text) text.textContent = "Henüz rapor gelmedi...";
            if (body) body.classList.add("hidden");
        }

        document.getElementById("verdict-placeholder").classList.remove("hidden");
        document.getElementById("verdict-content").classList.add("hidden");
        if (qaMessagesList) qaMessagesList.innerHTML = "";
    }

    // Poll Job Status
    function startPollingStatus(jobId) {
        if (pollInterval) clearInterval(pollInterval);

        pollInterval = setInterval(async () => {
            try {
                const res = await fetch(`/api/status/${jobId}`);
                if (!res.ok) return;

                const job = await res.json();
                updateUIWithJobState(job);

                if (job.status === "completed" || job.status === "failed") {
                    clearInterval(pollInterval);
                    statusSpinner.classList.add("hidden");
                }
            } catch (e) {
                console.error("Polling error:", e);
            }
        }, 2000);
    }

    // Update UI Elements
    function updateUIWithJobState(job) {
        statusText.textContent = job.current_step || "Ajanlar Çalışıyor...";

        // Update Agent-by-Agent Outputs with DOMPurify XSS Protection
        if (job.agent_outputs && job.agent_outputs.length > 0) {
            job.agent_outputs.forEach((out, idx) => {
                if (idx < 4) {
                    const badge = document.getElementById(`status-badge-${idx}`);
                    const body = document.getElementById(`agent-body-${idx}`);
                    const text = document.getElementById(`agent-text-${idx}`);

                    if (badge) {
                        badge.className = "agent-status-badge badge-done";
                        badge.textContent = "✅ Tamamlandı";
                    }
                    if (text && out.output) {
                        text.innerHTML = renderSafeMarkdown(out.output);
                    }
                    if (body && body.classList.contains("hidden")) {
                        body.classList.remove("hidden");
                    }
                }
            });
        }

        // Final Verdict Completed
        if (job.status === "completed" && job.final_report) {
            latestReportMarkdown = job.final_report;

            document.getElementById("verdict-placeholder").classList.add("hidden");
            document.getElementById("verdict-content").classList.remove("hidden");

            const judgeMarkdown = document.getElementById("judge-report-markdown");
            if (judgeMarkdown) {
                judgeMarkdown.innerHTML = renderSafeMarkdown(job.final_report);
            }

            const verdictBanner = document.getElementById("verdict-banner-box");
            const verdictTitle = document.getElementById("verdict-title-text");

            const reportUpper = job.final_report.toUpperCase();
            if (reportUpper.includes("CONDITIONAL GO") || reportUpper.includes("ŞARTLI")) {
                verdictBanner.className = "verdict-banner verdict-conditional";
                verdictTitle.textContent = "🟡 CONDITIONAL GO (ŞARTLI DEVAM)";
            } else if (reportUpper.includes("NO-GO") || reportUpper.includes("NO GO")) {
                verdictBanner.className = "verdict-banner verdict-nogo";
                verdictTitle.textContent = "🔴 NO-GO (DEVAM ETMEYİN)";
            } else {
                verdictBanner.className = "verdict-banner verdict-go";
                verdictTitle.textContent = "🟢 GO (DEVAM ET!)";
            }

            // Render Radar Chart with Scores
            renderRadarScoreChart(80, 75, 70, 75);

            statusText.textContent = "✅ Tüm Analizler Tamamlandı!";
        }

        if (job.status === "failed") {
            statusText.textContent = `❌ Hata: ${job.error || "Bilinmeyen hata"}`;
        }
    }

    // Chart.js Radar Score Chart Renderer
    function renderRadarScoreChart(market, demand, tech, financial) {
        const ctx = document.getElementById('scoreRadarChart');
        if (!ctx) return;

        if (radarChart) radarChart.destroy();

        radarChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Pazar Fırsatı (30%)', 'Talep Aciliyeti (25%)', 'Teknik Fizibilite (25%)', 'Finansal Uyum (20%)'],
                datasets: [{
                    label: 'Metrik Puanı',
                    data: [market, demand, tech, financial],
                    backgroundColor: 'rgba(124, 58, 237, 0.15)',
                    borderColor: '#7c3aed',
                    borderWidth: 2,
                    pointBackgroundColor: '#ffffff',
                    pointBorderColor: '#7c3aed',
                    pointHoverBackgroundColor: '#7c3aed',
                    pointHoverBorderColor: '#ffffff'
                }]
            },
            options: {
                scales: {
                    r: {
                        angleLines: { color: 'rgba(0, 0, 0, 0.1)' },
                        grid: { color: 'rgba(0, 0, 0, 0.1)' },
                        pointLabels: { color: '#0f172a', font: { size: 11, weight: '700' } },
                        ticks: { backdropColor: 'transparent', color: '#64748b', min: 0, max: 100 }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // 1-Click PDF Export
    if (downloadPdfBtn) {
        downloadPdfBtn.addEventListener("click", () => {
            const reportElement = document.getElementById("judge-verdict-card");
            if (!reportElement) return;

            const opt = {
                margin: 10,
                filename: `TSI_Feasibility_Report_${Date.now()}.pdf`,
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2 },
                jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
            };

            html2pdf().set(opt).from(reportElement).save();
        });
    }

    // 1-Click Markdown Download
    if (downloadMdBtn) {
        downloadMdBtn.addEventListener("click", () => {
            if (!latestReportMarkdown) return;
            const blob = new Blob([latestReportMarkdown], { type: "text/markdown;charset=utf-8;" });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = `TSI_Hakem_Raporu_${Date.now()}.md`;
            link.click();
        });
    }

    // Copy Report Button
    if (copyReportBtn) {
        copyReportBtn.addEventListener("click", () => {
            const markdownContainer = document.getElementById("judge-report-markdown");
            if (markdownContainer) {
                navigator.clipboard.writeText(markdownContainer.innerText);
                alert("🔒 Hakem Raporu panoya kopyalandı!");
            }
        });
    }

    // Interactive Q&A Chat with Judge Agent ("Hakeme Soru Sor")
    if (sendQuestionBtn && qaQuestionInput) {
        const sendQuestion = async () => {
            const question = qaQuestionInput.value.trim();
            if (!question || !currentJobId) return;

            // Render User Message
            const userMsgDiv = document.createElement("div");
            userMsgDiv.className = "qa-message qa-user";
            userMsgDiv.textContent = question;
            qaMessagesList.appendChild(userMsgDiv);

            qaQuestionInput.value = "";
            qaMessagesList.scrollTop = qaMessagesList.scrollHeight;

            // Render Loading Judge Message
            const loadingMsgDiv = document.createElement("div");
            loadingMsgDiv.className = "qa-message qa-judge";
            loadingMsgDiv.textContent = "Hakem Ajanı yanıtlıyor...";
            qaMessagesList.appendChild(loadingMsgDiv);

            try {
                const res = await fetch("/api/ask-judge", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        job_id: currentJobId,
                        question: question
                    })
                });

                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || "Yanıt alınamadı.");

                loadingMsgDiv.innerHTML = renderSafeMarkdown(data.answer);
            } catch (err) {
                loadingMsgDiv.textContent = `Hata: ${err.message}`;
            }
            qaMessagesList.scrollTop = qaMessagesList.scrollHeight;
        };

        sendQuestionBtn.addEventListener("click", sendQuestion);
        qaQuestionInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") sendQuestion();
        });
    }
});
