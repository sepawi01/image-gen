import PromptSelections from "./PromptSelections.tsx";
import PromptInput from "./PromptInput.tsx";


export default function PromptToolbar() {
  return (
    <div className="p-5">
      <PromptSelections/>
      <PromptInput/>
    </div>
  );
}