const { createApp, ref, computed, onMounted } = Vue;

const app = createApp({
    setup() {
        const pcaps = ref([]);
        const interfaces = ref([]);
        const selected = ref([]);
        const speedMbps = ref(0);
        const chosenInterface = ref("lo");
        const currentReplay = ref(null);
        const isReplaying = ref(false);
        const pollInterval = ref(null);

        const displaySpeed = computed(() => {
            return speedMbps.value === 0 ? "Unlimited (0 Mbps)" : `${speedMbps.value} Mbps`;
        });

        const replayStatus = computed(() => {
            if (isReplaying.value && currentReplay.value) {
                return `Replaying on ${currentReplay.value.interface} at ${currentReplay.value.speed_mbps} Mbps`;
            }
            return "Ready";
        });

        const formatSize = (size) => {
            if (size < 1024) return `${size} B`;
            if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
            return `${(size / (1024 * 1024)).toFixed(1)} MB`;
        };

        const pollStatus = async () => {
            if (!currentReplay.value) {
                isReplaying.value = false;
                return;
            }
            try {
                const res = await fetch(`/api/replay/${currentReplay.value.id}/status`);
                if (!res.ok) {
                    isReplaying.value = false;
                    currentReplay.value = null;
                    return;
                }
                const data = await res.json();
                currentReplay.value = data;
            } catch (e) {
                console.error("Poll error:", e);
                isReplaying.value = false;
                currentReplay.value = null;
            }
        };

        const loadPcaps = async () => {
            try {
                const res = await fetch("/api/pcaps");
                pcaps.value = await res.json();
            } catch (e) {
                console.error("Failed to load pcaps:", e);
            }
        };

        const loadInterfaces = async () => {
            try {
                const res = await fetch("/api/interfaces");
                interfaces.value = await res.json();
                if (interfaces.value.length > 0 && !chosenInterface.value) {
                    chosenInterface.value = interfaces.value[0].name;
                }
            } catch (e) {
                console.error("Failed to load interfaces:", e);
            }
        };

        const toggleSelect = (name) => {
            const idx = selected.value.indexOf(name);
            if (idx > -1) {
                selected.value.splice(idx, 1);
            } else {
                selected.value.push(name);
            }
        };

        const handleFileUpload = async (e) => {
            const files = e.target.files;
            if (!files || files.length === 0) return;

            for (const file of files) {
                const formData = new FormData();
                formData.append("file", file);

                try {
                    const res = await fetch("/api/pcaps", {
                        method: "POST",
                        body: formData
                    });
                    if (res.ok) {
                        await loadPcaps();
                    }
                } catch (err) {
                    console.error("Upload failed:", err);
                }
            }
            e.target.value = "";
        };

        const deleteSelected = async () => {
            if (selected.value.length === 0) return;
            
            for (const name of selected.value) {
                try {
                    await fetch(`/api/pcaps/${name}`, { method: "DELETE" });
                } catch (e) {
                    console.error(`Failed to delete ${name}:`, e);
                }
            }
            selected.value = [];
            await loadPcaps();
        };

        const startReplay = async () => {
            if (selected.value.length === 0) return;

            try {
                const res = await fetch("/api/replay", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        files: selected.value,
                        interface: chosenInterface.value,
                        speed: speedMbps.value
                    })
                });
                const data = await res.json();
                if (data.id) {
                    currentReplay.value = { id: data.id };
                    isReplaying.value = true;
                    pollInterval.value = setInterval(pollStatus, 2000);
                }
            } catch (e) {
                console.error("Failed to start replay:", e);
            }
        };

        const stopReplay = async () => {
            if (!currentReplay.value) return;

            try {
                await fetch(`/api/replay/${currentReplay.value.id}`, { method: "DELETE" });
                currentReplay.value = null;
                isReplaying.value = false;
                if (pollInterval.value) {
                    clearInterval(pollInterval.value);
                    pollInterval.value = null;
                }
            } catch (e) {
                console.error("Failed to stop replay:", e);
            }
        };

        onMounted(() => {
            loadPcaps();
            loadInterfaces();
        });

        return {
            pcaps,
            interfaces,
            selected,
            speedMbps,
            chosenInterface,
            currentReplay,
            isReplaying,
            displaySpeed,
            replayStatus,
            formatSize,
            toggleSelect,
            handleFileUpload,
            deleteSelected,
            startReplay,
            stopReplay
        };
    }
});

app.mount("#app");
