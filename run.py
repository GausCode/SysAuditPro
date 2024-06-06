from sysauditpro.auditor import perform_audit
from sysauditpro.reporter import generate_report, save_report

def main():
    # Create security audit
    audit_results = perform_audit()

    # Generate pdf report from events
    report_file = generate_report(audit_results)

    # save the file
    save_report(report_file)

    print(f"The report successfully save as: {report_file}")

if __name__ == '__main__':
    main()
