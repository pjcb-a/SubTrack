<script setup>
import { ref } from 'vue';
import { useSubscriptions } from '../../composables/useSubscriptions';
import { useUserSettings } from '../../composables/useUserSettings';

const fileInput = ref(null);
const historyError = ref('');
const actionError = ref('');
const actionStatus = ref('');

const { deletedSubscriptions, clearDeletedSubscriptions } = useSubscriptions();
const {
  settingsSaving,
  importResult,
  exportSubscriptionsCsv,
  importSubscriptionsCsv,
  clearImportResult,
} = useUserSettings();

const clearHistory = async () => {
  historyError.value = '';

  if (!confirm('Are you sure you want to permanently clear all history records?')) {
    return;
  }

  try {
    await clearDeletedSubscriptions();
  } catch (error) {
    historyError.value = error.message;
  }
};

const handleExport = async () => {
  actionError.value = '';
  actionStatus.value = '';

  try {
    await exportSubscriptionsCsv();
    actionStatus.value = 'CSV exported successfully.';
  } catch (error) {
    actionError.value = error.message;
  }
};

const openFilePicker = () => {
    fileInput.value?.click();
};

const handleImport = async (event) => {
  actionError.value = '';
  actionStatus.value = '';
  clearImportResult();

  const [file] = event.target.files || [];
  if (!file) {
    return;
  }

  try {
    const result = await importSubscriptionsCsv(file);
    actionStatus.value = `Import complete. Added ${result.created_count} row(s), skipped ${result.skipped_count}.`;
  } catch (error) {
    actionError.value = error.message;
  } finally {
    event.target.value = '';
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
        <button class="settings-btn-secondary" :disabled="settingsSaving" @click="handleExport">Export</button>
      </div>

      <div class="data-panel">
        <i class="fa-solid fa-file-import"></i>
        <div class="panel-text">
          <span>Import Data</span>
          <p>Upload a CSV to bulk-add subscriptions.</p>
        </div>
        <button class="settings-btn-secondary" :disabled="settingsSaving" @click="openFilePicker">Import</button>
        <input ref="fileInput" type="file" accept=".csv,text/csv" class="hidden-input" @change="handleImport">
      </div>
    </div>

    <p v-if="actionStatus" class="status-ok">{{ actionStatus }}</p>
    <p v-if="actionError" class="error-text">{{ actionError }}</p>

    <div v-if="importResult" class="import-summary">
      <p><strong>Created:</strong> {{ importResult.created_count }}</p>
      <p><strong>Skipped:</strong> {{ importResult.skipped_count }}</p>
      <p><strong>Warnings:</strong> {{ importResult.warning_count }}</p>
    </div>

    <div class="history-clear">
      <div class="clear-text">
        <span>Clean Up History</span>
        <p>This will permanently remove all items from your deleted history.</p>
        <p v-if="historyError" class="error-text">{{ historyError }}</p>
      </div>

      <button v-if="deletedSubscriptions.length === 0" class="clear-btn-locked"> <i class="fa-solid fa-history"></i> No History</button>

      <button v-else class="clear-btn" @click="clearHistory">
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
  margin-bottom: 25px;
}

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
  margin-top: 16px;
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

.hidden-input {
  display: none;
}

.status-ok {
  color: var(--app-accent-strong);
  font-weight: 600;
}

.error-text {
  color: var(--app-danger);
}

.import-summary {
  padding: 14px 16px;
  border-radius: 14px;
  background: var(--app-surface-alt);
  border: 1px solid var(--app-border);
}

.import-summary p {
  margin: 0 0 6px;
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
