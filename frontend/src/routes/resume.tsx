import { createFileRoute, useRouter } from "@tanstack/react-router";
import { useState } from "react";

export const Route = createFileRoute("/resume")({
  component: REsumePage,
});

function REsumePage() {


  return (
   <div>hello</div>
  );
}