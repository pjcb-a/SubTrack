<script setup>
import { ref } from 'vue';
import { useSubscriptions } from '../../composables/useSubscriptions';
import { useUserSettings } from '../../composables/useUserSettings';

const { deletedSubscriptions, clearDeletedSubscriptions } = useSubscriptions();
const {
  exportSubscriptionsCsv,
  importSubscriptionsCsv,
  importResult,
  settingsSaving,
} = useUserSettings();
const historyError = ref('');
const dataError = ref('');
const localMessage = ref('');
const selectedFile = ref(null);

const clearHistory = async () => {
  historyError.value = '';

  if (confirm('Are you sure you want to permanently clear all history records?')) {
    try {
      await clearDeletedSubscriptions();
    } catch (error) {
      historyError.value = error.message;
    }
  }
};

const handleExport = async () => {
  dataError.value = '';
  localMessage.value = '';

  try {
    await exportSubscriptionsCsv();
    localMessage.value = 'CSV export downloaded.';
  } catch (error) {
    dataError.value = error.message;
  }
};

const handleFileChange = (event) => {
  selectedFile.value = event.target.files?.[0] ?? null;
};

const handleImport = async () => {
  dataError.value = '';
  localMessage.value = '';

  try {
    await importSubscriptionsCsv(selectedFile.value);
    localMessage.value = 'Import completed.';
  } catch (error) {
    dataError.value = error.message;
  }
};
</script>

<template>
  <section class="settings-card">
    <div class="card-header">
      <h3><i class="fa-solid fa-database"></i> Data Management</h3>
    </div>

    <div class="data-grid">
      <div class="data-panel">
        <i class="fa-solid fa-file-export"></i>
        <div class="panel-text">
          <span>Export Data</span>
          <p>Download your subscriptions as a CSV file.</p>
        </div>
        <button class="settings-btn-secondary" :disabled="settingsSaving" @click="handleExport">
          {{ settingsSaving ? 'Working...' : 'Export' }}
        </button>
      </div>

      <div class="data-panel">
        <i class="fa-solid fa-file-import"></i>
        <div class="panel-text">
          <span>Import Data</span>
          <p>Upload a CSV to bulk-add subscriptions.</p>
        </div>
        <input class="file-input" type="file" accept=".csv,text/csv" @change="handleFileChange" />
        <button class="settings-btn-secondary" :disabled="settingsSaving || !selectedFile" @click="handleImport">
          {{ settingsSaving ? 'Working...' : 'Import' }}
        </button>
      </div>
    </div>

    <p v-if="dataError" class="feedback error">{{ dataError }}</p>
    <p v-else-if="localMessage" class="feedback success">{{ localMessage }}</p>

    <div v-if="importResult" class="import-summary">
      <span>Import Result</span>
      <p>Created: {{ importResult.created_count }} | Skipped: {{ importResult.skipped_count }} | Warnings: {{ importResult.warning_count }}</p>
      <ul class="import-list">
        <li v-for="rowResult in importResult.row_results.slice(0, 10)" :key="`${rowResult.row}-${rowResult.status}`">
          Row {{ rowResult.row }}: {{ rowResult.reason }}
        </li>
      </ul>
    </div>

    <div class="history-clear">
      <div class="clear-text">
        <span>Clean Up History</span>
        <p>This will permanently remove all items from your deleted history.</p>
        <p v-if="historyError" class="feedback error"> {{ historyError }}</p>
      </div>


      <button v-if="deletedSubscriptions.length === 0" class="clear-btn-locked"> <i class="fa-solid fa-history"></i> No History</button>
     
      <button v-if="deletedSubscriptions.length > 0" class="clear-btn" @click="clearHistory">
            <i class="fa-solid fa-trash"></i> Clear History
        </button>
    </div>
  </section>
</template>

<style scoped>
.data-grid { 
  display: grid; 
  grid-template-columns: 1fr 1fr; 
  gap: 15px; 
  margin-bottom: 25px; }

.data-panel {
  background: var(--app-surface-alt); 
  padding: 20px; 
  border-radius: 16px;
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  text-align: center; 
  gap: 12px;
}

.data-panel i { 
  font-size: 1.4rem; 
  color: var(--app-accent); 
}

.panel-text span { 
  font-weight: 700; 
  color: var(--app-text); 
  font-size: 0.9rem; 
}

.panel-text p { 
  font-size: 0.75rem; 
  color: var(--app-text-muted); 
  margin-top: 4px; 
}

.history-clear {
  display: flex; 
  justify-content: space-between; 
  align-items: center;
  background: var(--app-surface-alt); 
  padding: 20px; 
  border-radius: 16px;
}

.clear-text span { 
  font-weight: 700; 
  color: var(--app-text); 
}

.clear-text p { 
  font-size: 0.8rem; 
  color: var(--app-text-muted); 
}

.settings-btn-secondary {
  background-color: var(--app-surface-alt);
  border: 2px solid var(--app-border);
  color: var(--app-text); 
  padding: 10px 20px; 
  border-radius: 12px;
  font-weight: 600; 
  cursor: pointer; 
  transition: 0.2s;
}

.settings-btn-secondary:hover {
  background-color: var(--app-accent-strong);
  color: #f5f5f5;
  border-color: transparent;
  transform: translateY(-1px);
}

.settings-btn-secondary:disabled,
.clear-btn:disabled {
  opacity: 0.7;
  cursor: wait;
}

.file-input {
  width: 100%;
  font-size: 0.75rem;
}

.import-summary {
  background: var(--app-surface-alt);
  padding: 18px;
  border-radius: 16px;
  margin-bottom: 25px;
}

.import-summary span {
  font-weight: 700;
  color: var(--app-text);
}

.import-summary p {
  margin-top: 6px;
  font-size: 0.8rem;
  color: var(--app-text-muted);
}

.import-list {
  margin: 10px 0 0;
  padding-left: 18px;
  color: var(--app-text);
  font-size: 0.82rem;
}

.feedback {
  font-size: 0.82rem;
}

.feedback.error {
  color: var(--app-danger);
}

.feedback.success {
  color: var(--app-accent);
}

.clear-btn {
  background: transparent;
  border: 1px solid var(--app-danger);
  color: var(--app-danger);
  padding: 8px 16px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
}

.clear-btn-locked {
  cursor: not-allowed;
  background: transparent;
  border: 2px solid var(--app-text-muted);
  color: var(--app-text-muted);
  padding: 8px 16px;
  border-radius: 10px;
  font-weight: 600;
}

.clear-btn:hover {
  background: var(--app-danger);
  color: white;
}

@media (max-width: 700px) {
  .data-grid { 
    grid-template-columns: 1fr; 
  }

  .history-clear { 
    flex-direction: column; 
    text-align: center; 
    gap: 15px; 
  }
}
</style>
