from sysauditpro.auditor import perform_audit
from sysauditpro.reporter import generate_report, save_report

def main():
    # Führe das Sicherheitsaudit durch
    audit_results = perform_audit()

    # Generiere einen PDF-Bericht basierend auf den Audit-Ergebnissen
    report_file = generate_report(audit_results)

    # Optional: Speichere oder sende den Bericht
    save_report(report_file)

    print(f"Der Bericht wurde erfolgreich erstellt und gespeichert als: {report_file}")

if __name__ == '__main__':
    main()
