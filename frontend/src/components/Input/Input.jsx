function Input({
  label,
  type = "text",
  placeholder,
  value,
  onChange,
}) {
  return (
    <div className="flex flex-col gap-2">
      <label className="font-medium text-slate-700">
        {label}
      </label>

      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className="
          border
          border-slate-300
          rounded-xl
          px-4
          py-3
          outline-none
          focus:border-blue-600
          focus:ring-2
          focus:ring-blue-200
          transition
        "
      />
    </div>
  );
}

export default Input;