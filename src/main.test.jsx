import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { EmptyState, KpiGrid, NoFinancialRecords, economicHistoryRows, economicValue, labelize } from "./main.jsx";

function IconStub() {
  return <span data-testid="icon" />;
}

describe("QuantGuard frontend components", () => {
  it("renders empty states with clear copy", () => {
    render(<EmptyState title="No records yet" text="Upload data to begin." />);
    expect(screen.getByRole("heading", { name: "No records yet" })).toBeInTheDocument();
    expect(screen.getByText("Upload data to begin.")).toBeInTheDocument();
  });

  it("renders KPI cards", () => {
    render(<KpiGrid data={[["Risk Score", 74, "/100", "High Risk", "#ff3d43", IconStub]]} />);
    expect(screen.getByText("Risk Score")).toBeInTheDocument();
    expect(screen.getByText("/100")).toBeInTheDocument();
    expect(screen.getByText("High Risk")).toBeInTheDocument();
  });

  it("builds chart rows from economic history", () => {
    const rows = economicHistoryRows({
      "Inflation Rate": [{ date: "2026-05-01", value: 22.1 }],
      "Fuel Price Index": [{ date: "2026-05-01", value: 123.1 }],
    });
    expect(rows).toEqual([{ date: "2026-05-01", "Inflation Rate": 22.1, "Fuel Price Index": 123.1 }]);
  });

  it("routes users with missing financial data to upload", () => {
    const go = vi.fn();
    render(<NoFinancialRecords go={go} />);
    screen.getByRole("button", { name: /go to upload data/i }).click();
    expect(go).toHaveBeenCalledWith("upload");
  });

  it("formats labels from identifiers", () => {
    expect(labelize("risk_assessment_report")).toBe("Risk Assessment Report");
  });

  it("formats NGN economic indicators with realistic precision", () => {
    expect(economicValue({ name: "Official USD/NGN", value: 1374.69, unit: "NGN" })).toBe("₦1,374.69");
    expect(economicValue({ name: "Parallel USD/NGN", value: 1400, unit: "NGN" })).toBe("₦1,400");
  });
});
